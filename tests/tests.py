from django.test import TestCase
from django.test.utils import override_settings
from django.core import mail
from django.apps import apps
from django.conf import settings
from backends import console, database, filebased
from models import Email, Recipient
from mock import patch
from django.urls import reverse
import os, shutil


class ModelTestCase(TestCase):
    def test_create_email(self):
        recipient = Recipient.objects.create(
            email='me@me.com'
        )

        email = Email.objects.create(
            subject='Test subject',
            plaintext_message='Test message',
            from_email='test@testuser.com'
        )
        email.recipients.add(recipient)

        self.assertEqual(Recipient.objects.all().count(), 1)
        self.assertEqual(Email.objects.all().count(), 1)
        self.assertEqual(email.recipients.all().count(), 1)

    def test_create_email_multiple_recipients(self):
        email = Email.objects.create(
            subject='Test subject',
            plaintext_message='Test message',
            from_email='test@testuser.com'
        )

        recipients = [
            'testuser1@test.com',
            'testuser2@test.com',
            'testuser3@test.com'
        ]

        for recipient_email in recipients:
            recipient = Recipient.objects.create(
                email=recipient_email
            )
            email.recipients.add(recipient)

        self.assertEqual(Recipient.objects.all().count(), 3)

        for recipient_email in recipients:
            self.assertTrue(Email.objects.filter(recipients__email=recipient_email).exists())

    def test_create_recipient(self):
        Recipient.objects.create(
            email='me@me.com'
        )

        self.assertEqual(Recipient.objects.all().count(), 1)

    def test_recipient_count(self):
        recipient = Recipient.objects.create(
            email='me@me.com'
        )

        email = Email.objects.create(
            subject='Test subject',
            plaintext_message='Test message',
            from_email='test@testuser.com'
        )
        email.recipients.add(recipient)

        self.assertEqual(email.total_recipients(), 1)

    @override_settings(MAILTRAIL_RECIPIENT_MODEL='mailtrail.DummyRecipient',
                       MAILTRAIL_RECIPIENT_MODEL_ATTRIBUTE='email_address')
    def test_custom_recipient_model(self):
        Model = apps.get_model(settings.MAILTRAIL_RECIPIENT_MODEL)
        data = {
            settings.MAILTRAIL_RECIPIENT_MODEL_ATTRIBUTE: 'test@testuser.com',
            'name': 'Mr. T. Esting'
        }
        recipient = Model.objects.create(**data)

        self.assertEqual(recipient.email_address, 'test@testuser.com')
        self.assertEqual(recipient.name, 'Mr. T. Esting')
        self.assertEqual(Model.objects.all().count(), 1)


class BackendTestCase(TestCase):
    FILE_TEST_PATH = '/tmp/mailtrail-tests'

    @patch('django.core.mail.backends.locmem.EmailBackend', console.EmailBackend)
    def test_send_email_console(self):
        mail.send_mail('Test subject', 'Test message', 'test@testuser.com', ('test@testuser.com',), html_message='<p>html</p>')

        all_emails = Email.objects.all()
        self.assertEquals(all_emails.count(), 1)

        email = all_emails.first()
        self.assertEquals(email.subject, 'Test subject')
        self.assertEquals(email.html_message, '<p>html</p>')
        self.assertEquals(email.from_email, 'test@testuser.com')
        self.assertEquals(Recipient.objects.all().count(), 1)

    @patch('django.core.mail.backends.locmem.EmailBackend', console.EmailBackend)
    def test_send_email_duplicate_recipients(self):
        mail.send_mail('Test subject', 'Test message', 'test@testuser.com',
                       ('test@testuser.com', 'test@testuser.com', 'test2@testuser.com'),
                       html_message='<p>html</p>')

        self.assertEquals(Email.objects.all().count(), 1)

        email = Email.objects.all().first()
        self.assertEqual(email.recipients.all().count(), 2)

        self.assertEqual(Recipient.objects.filter(email='test@testuser.com').count(), 1)
        self.assertEqual(Recipient.objects.filter(email='test2@testuser.com').count(), 1)

    @patch('django.core.mail.backends.locmem.EmailBackend', database.EmailBackend)
    def test_send_email_database(self):
        mail.send_mail('Test subject', 'Test message', 'test@testuser.com', ('test@testuser.com',),
                       html_message='<p>html</p>')

        self.assertEquals(Email.objects.all().count(), 1)

        email = Email.objects.all().first()
        self.assertEqual(email.recipients.all().count(), 1)

        self.assertEqual(Recipient.objects.filter(email='test@testuser.com').count(), 1)

    @patch('django.core.mail.backends.locmem.EmailBackend', filebased.EmailBackend)
    @override_settings(EMAIL_FILE_PATH=FILE_TEST_PATH)
    def test_send_email_database(self):
        mail.send_mail('Test subject', 'Test message', 'test@testuser.com', ('test@testuser.com',),
                       html_message='<p>html</p>')

        self.assertEquals(Email.objects.all().count(), 1)

        email = Email.objects.all().first()
        self.assertEqual(email.recipients.all().count(), 1)
        self.assertEqual(Recipient.objects.filter(email='test@testuser.com').count(), 1)

        num_files = len([f for f in os.listdir(self.FILE_TEST_PATH)])
        self.assertEqual(num_files, 1)

    @patch('django.core.mail.backends.locmem.EmailBackend', database.EmailBackend)
    def test_resend_email(self):
        mail.send_mail('Test subject', 'Test message', 'test@testuser.com',
                       ('test@testuser.com', 'test@testuser.com', 'test2@testuser.com'),
                       html_message='<p>html</p>')

        self.assertEqual(Email.objects.all().count(), 1)

        email = Email.objects.all().first()
        url = reverse('admin:mailtrail_email_resend', kwargs={'pk': email.pk})
        response = self.client.post(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Email.objects.all().count(), 2)

    @patch('django.core.mail.backends.locmem.EmailBackend', database.EmailBackend)
    def test_send_empty_email(self):
        mail.send_mail('Test subject', '', 'test@testuser.com',
                       ('test@testuser.com', 'test@testuser.com', 'test2@testuser.com'),
                       html_message='')

        self.assertEqual(Email.objects.all().count(), 1)

        mail.send_mail('Test subject', 'empty html', 'test@testuser.com',
                       ('test@testuser.com', 'test@testuser.com', 'test2@testuser.com'),
                       html_message='')

        self.assertEqual(Email.objects.all().count(), 2)

        mail.send_mail('Test subject', '', 'test@testuser.com',
                       ('test@testuser.com', 'test@testuser.com', 'test2@testuser.com'),
                       html_message='empty plaintext')

        self.assertEqual(Email.objects.all().count(), 3)

    def tearDown(self):
        if os.path.exists(self.FILE_TEST_PATH):
            shutil.rmtree(self.FILE_TEST_PATH)

        super(BackendTestCase, self).tearDown()
