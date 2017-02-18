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


class BackendTestCase(TestCase):
    @patch('django.core.mail.backends.locmem.EmailBackend', console.EmailBackend)
    def test_send_email_locmem(self):
        mail.send_mail('Test subject', 'Test message', 'test@testuser.com', ('test@testuser.com',), html_message='<p>html</p>')

        all_emails = Email.objects.all()
        self.assertEquals(all_emails.count(), 1)

        email = all_emails.first()
        self.assertEquals(email.subject, 'Test subject')
        self.assertEquals(email.html_message, '<p>html</p>')
        self.assertEquals(email.from_email, 'test@testuser.com')
