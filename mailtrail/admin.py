from django.contrib import admin
from django.conf.urls import url
from mailtrail.models import Email, get_recipient_model, get_recipient_model_attribute
from mailtrail import views


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    change_form_template = 'email/change.html'

    list_display = ['subject', 'recipient_list', 'created']
    list_filter = ['recipients__{}'.format(get_recipient_model_attribute()), 'created', 'backend']
    exclude = []
    readonly_fields = ['payload', 'plaintext_message', 'html_message', 'created', 'from_email', 'subject', 'backend']

    def change_view(self, request, object_id, **kwargs):
        kwargs['extra_context'] = {
            'pk': object_id
        }
        return super(EmailAdmin, self).change_view(request, object_id, **kwargs)

    def get_urls(self):
        urls = super(EmailAdmin, self).get_urls()
        my_urls = [
            url(r'^(?P<pk>[0-9a-f-]+)/resend/$', views.EmailResendView.as_view(), name="mailtrail_email_resend")
        ]
        return my_urls + urls
