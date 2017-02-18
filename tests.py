from django.test import TestCase
from django.core import mail
from backends import console
from models import Email, Recipient
from mock import patch


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


class BackendTestCase(TestCase):
    @patch('django.core.mail.backends.locmem.EmailBackend', console.EmailBackend)
    def test_send_email_console(self):
        mail.send_mail('Test subject', 'Test message', 'test@testuser.com', ('test@testuser.com',), html_message='<p>html</p>')

        all_emails = Email.objects.all()
        self.assertEquals(all_emails.count(), 1)

        email = all_emails.first()
        self.assertEquals(email.subject, 'Test subject')
        self.assertEquals(email.html_message, '<p>html</p>')
        self.assertEquals(email.from_email, 'test@testuser.com')

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

