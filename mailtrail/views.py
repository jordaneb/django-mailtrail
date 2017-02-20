from django.views.generic import View
from django.template.response import TemplateResponse
from django.core import urlresolvers
from django.shortcuts import get_object_or_404, HttpResponseRedirect
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


class EmailRawView(View):
    def get(self, request, pk):
        email = get_object_or_404(Email, pk=pk)

        context = {
            'email': email,
            'bytes': len(email.payload)
        }

        return TemplateResponse(request, template='email/raw.html', context=context)


class EmailForwardView(View):
    def get(self, request, pk):
        email = get_object_or_404(Email, pk=pk)

        context = {
            'email': email
        }

        return TemplateResponse(request, template='email/forward.html', context=context)

    def post(self, request, pk):
        email = get_object_or_404(Email, pk=pk)

        data = request.POST

        recipients = data['recipients_new'].replace(' ', '').split(',')
        if 'include_recipients' in data.keys():
            [recipients.append(recipient.email) for recipient in email.recipients.all()]

        mail.send_mail(email.subject, email.plaintext_message, email.from_email,
                       recipients, html_message=email.html_message)

        forwarded_email = Email.objects.all().order_by('created').first()
        forwarded_email.is_forwarded = True
        forwarded_email.save()

        context = {
            'email': email
        }

        return HttpResponseRedirect(urlresolvers.reverse('admin:mailtrail_email_change', args=(forwarded_email.pk,)))
