from django.test import TestCase, override_settings
from django.db import models
from models import Email, Recipient


class ModelTestCase(TestCase):
    def test_create_email(self):
        recipient = Recipient.objects.create(
            email='me@me.com'
        )

        email = Email.objects.create(
            subject='Test subject',
            message='Test message',
            from_email='test@testuser.com'
        )
        email.recipients.add(recipient)

        self.assertEqual(Recipient.objects.all().count(), 1)
        self.assertEqual(Email.objects.all().count(), 1)
        self.assertEqual(email.recipients.all().count(), 1)
