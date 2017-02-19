from django.db import models
from django.apps import apps
from django.conf import settings
from django.utils import timezone
import uuid


class Recipient(models.Model):
    """
    This recipient model can be extended if you would like to link emails to
    user models. However, the `email` field must always be present and all
    other fields should be nullable.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email


def get_recipient_model():
    return getattr(settings, 'MAILTRAIL_RECIPIENT_MODEL', Recipient)


class Email(models.Model):
    """
    Email model for catching and storing all sent emails via `django.core.mail`.
    """
    RECIPIENT_MODEL = get_recipient_model()

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subject = models.CharField(max_length=255, blank=True)
    payload = models.TextField(blank=True)
    plaintext_message = models.TextField(blank=True)
    html_message = models.TextField(blank=True, null=True)
    from_email = models.EmailField()
    recipients = models.ManyToManyField(RECIPIENT_MODEL, related_name='emails')

    # An identifier to track what backend was used
    backend = models.CharField(max_length=32, null=True, blank=True)

    # When the email was first sent
    created = models.DateTimeField(default=timezone.now)

    def total_recipients(self):
        return self.recipients.all().count()

    def recipient_list(self):
        total_recipients = self.total_recipients()
        recipient_emails = ', '.join(recipient.email for recipient in self.recipients.all()[:3])

        if total_recipients > 3:
            recipient_emails += ' and {} more...'.format(total_recipients - 3)

        return recipient_emails

    def __str__(self):
        return '[{subject}] {recipients}'.format(
            subject=self.subject,
            recipients=self.recipient_list()
        )

    class Meta:
        ordering = ['subject', 'created']
