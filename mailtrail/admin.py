from django.contrib import admin
from django.conf.urls import url
from mailtrail.models import Email, get_recipient_model
from mailtrail import views


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    exclude = []
    readonly_fields = ['payload', 'plaintext_message', 'html_message', 'created', 'from_email', 'subject', 'backend']

    def get_urls(self):
        urls = super(EmailAdmin, self).get_urls()
        my_urls = [
            url(r'^(?P<pk>[0-9a-f-]+)/resend/$', views.EmailResendView.as_view(), name="resend_email")
        ]
        return my_urls + urls
