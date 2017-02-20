from django.contrib import admin
from django.conf import settings
from django.conf.urls import url
from mailtrail.models import Email, get_recipient_model, get_recipient_model_attribute
from mailtrail import views


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    change_form_template = 'email/change.html'

    exclude = ['payload']

    # Email are immutable
    readonly_fields = ['plaintext_message', 'html_message', 'created', 'from_email',
                       'subject', 'backend', 'recipients', 'is_forwarded']

    list_display = ['subject', 'recipient_list', 'created']
    list_filter = ['recipients__{}'.format(get_recipient_model_attribute()), 'created', 'backend']

    def change_view(self, request, object_id, **kwargs):
        kwargs['extra_context'] = {
            'pk': object_id  # Used for additional buttons
        }
        return super(EmailAdmin, self).change_view(request, object_id, **kwargs)

    def get_urls(self):
        """
        Add the MailTrail admin views
        """
        urls = super(EmailAdmin, self).get_urls()
        return [
            url(r'^(?P<pk>[0-9a-f-]+)/resend/$', views.EmailResendView.as_view(), name="mailtrail_email_resend"),
            url(r'^(?P<pk>[0-9a-f-]+)/raw/$', views.EmailRawView.as_view(), name="mailtrail_email_raw"),
            url(r'^(?P<pk>[0-9a-f-]+)/forward/$', views.EmailForwardView.as_view(), name="mailtrail_email_forward")
        ] + urls


class RecipientAdmin(admin.ModelAdmin):
    """
    Default RecipientModel admin used for basic viewing
    and modification of Recipient models.
    """
    exclude = []
    readonly_fields = [get_recipient_model_attribute()]


def get_recipient_model_admin():
    """
    Get the model admin for the Recipient model.
    """
    if hasattr(settings, 'MAILTRAIL_RECIPIENT_MODEL_ADMIN'):
        return getattr(settings, 'MAILTRAIL_RECIPIENT_MODEL_ADMIN')
    else:
        return RecipientAdmin


# Register the recipient model and model admin
admin.site.register(get_recipient_model(), get_recipient_model_admin())
