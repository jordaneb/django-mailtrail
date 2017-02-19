from django.views.generic import View
from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404
from django.core import mail
from mailtrail.models import Email, get_recipient_model_attribute


class EmailResendView(View):
    def get(self, request, pk):
        email = get_object_or_404(Email, pk=pk)
        recipients = email.recipients.all()

        context = {
            'email': email,
            'recipients': {
                'list': [getattr(recipient, get_recipient_model_attribute()) for recipient in recipients],
                'total': recipients.count()
            }
        }

        return TemplateResponse(request, template='email/resend.html', context=context)

    def post(self, request, pk):
        email = get_object_or_404(Email, pk=pk)
        recipients = email.recipients.all()

        total_recipients = recipients.count()

        context = {
            'email': email,
            'recipients': {
                'list': [getattr(recipient, get_recipient_model_attribute()) for recipient in recipients],
                'total': total_recipients
            },
            'messages': [
                'Successfully resent email to {} recipient{}'.format(total_recipients, 's' if total_recipients != 1 else '')
            ]
        }

        mail.send_mail(email.subject, email.plaintext_message, email.from_email,
                       email.recipients.all(), html_message=email.html_message)

        return TemplateResponse(request, template='email/resend.html', context=context)
