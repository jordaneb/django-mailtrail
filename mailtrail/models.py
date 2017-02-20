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


def get_recipient_model(as_instance=True):
    if not hasattr(settings, 'MAILTRAIL_RECIPIENT_MODEL'):
        return Recipient
    else:
        model = getattr(settings, 'MAILTRAIL_RECIPIENT_MODEL')
        if as_instance:
            return apps.get_model(model)
        else:
            return model


def get_recipient_model_attribute():
    return getattr(settings, 'MAILTRAIL_RECIPIENT_MODEL_ATTRIBUTE', 'email')



class Email(models.Model):
    """
    Email model for catching and storing all sent emails via `django.core.mail`.
    """
    RECIPIENT_MODEL = get_recipient_model(as_instance=False)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subject = models.CharField(max_length=255, blank=True)
    payload = models.TextField(blank=True)
    plaintext_message = models.TextField(blank=True)
    html_message = models.TextField(blank=True, null=True)
    from_email = models.EmailField()
    recipients = models.ManyToManyField(RECIPIENT_MODEL, related_name='emails')

    is_forwarded = models.BooleanField(default=False)

    # An identifier to track what backend was used
    backend = models.CharField(max_length=32, null=True, blank=True)

    # When the email was first sent
    created = models.DateTimeField(default=timezone.now)

    def total_recipients(self):
        return self.recipients.all().count()

    def recipient_list(self):
        total_recipients = self.total_recipients()
        recipient_emails = ', '.join(getattr(recipient, get_recipient_model_attribute()) for recipient in self.recipients.all()[:3])

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



# # # # # # # # # # # # #
#   ** TEST MODELS **   #
# # # # # # # # # # # # #

class DummyRecipient(models.Model):
    """
    Dummy recipient model for testing custom recipient model. Please
    don't reference this in production.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email_address = models.EmailField()
    name = models.CharField(max_length=50)

    def __str__(self):
        return '{} - {}'.format(self.email_address, self.name)
