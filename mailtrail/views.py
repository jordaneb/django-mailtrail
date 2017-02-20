from django.views.generic import View
from django.template.response import TemplateResponse
from django.core import urlresolvers
from django.shortcuts import get_object_or_404, HttpResponseRedirect
from django.core import mail
from mailtrail.models import Email, get_recipient_model_attribute


class SendEmailMixin:
    """
    Make sending email a bit more consistent
    """
    def send_email(self, obj):
        mail.send_mail(obj.subject, obj.plaintext_message, obj.from_email,
                       obj.recipients.all(), html_message=obj.html_message)


class EmailResendView(SendEmailMixin, View):
    """
    Resend an email to all existing recipients
    """
    def get(self, request, pk):
        email = get_object_or_404(Email, pk=pk)

        context = {
            'email': email,
            'recipients': {
                'list': [getattr(recipient, get_recipient_model_attribute()) for recipient in email.recipients.all()]
            }
        }

        return TemplateResponse(request, template='email/resend.html', context=context)

    def post(self, request, pk):
        email = get_object_or_404(Email, pk=pk)
        recipients = email.recipients.all()

        context = {
            'email': email,
            'recipients': {
                'list': [getattr(recipient, get_recipient_model_attribute()) for recipient in recipients]
            },
            'messages': [
                'Successfully resent email to {} recipient{}'.format(recipients.count(), 's' if recipients.count() != 1 else '')
            ]
        }

        self.send_email(email)

        return TemplateResponse(request, template='email/resend.html', context=context)


class EmailRawView(View):
    """
    View the raw payload of an email
    """
    def get(self, request, pk):
        email = get_object_or_404(Email, pk=pk)

        context = {
            'email': email,
            'bytes': len(email.payload)  # Total email size in bytes
        }

        return TemplateResponse(request, template='email/raw.html', context=context)


class EmailForwardView(SendEmailMixin, View):
    """
    Forward an email to existing and or new recipients
    """
    def get(self, request, pk):
        email = get_object_or_404(Email, pk=pk)

        context = {
            'email': email
        }

        return TemplateResponse(request, template='email/forward.html', context=context)

    def post(self, request, pk):
        email = get_object_or_404(Email, pk=pk)

        data = request.POST

        recipients = data['recipients_new'].replace(' ', '').split(',')  # Convert comma separated to list
        if 'include_recipients' in data.keys():
            # Get all existing recipient emails as list
            [recipients.append(recipient.email) for recipient in email.recipients.all()]

        self.send_email(email)  # Send the new email

        forwarded_email = Email.objects.all().order_by('created').first()
        forwarded_email.is_forwarded = True  # Identify this email as forwarded
        forwarded_email.save()

        # Redirect to forwarded email
        return HttpResponseRedirect(urlresolvers.reverse('admin:mailtrail_email_change', args=(forwarded_email.pk,)))
