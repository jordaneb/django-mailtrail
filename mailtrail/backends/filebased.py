from mailtrail.backends.base import MailTrailBase
from django.conf import settings
from django.core.mail.backends.filebased import EmailBackend as FileBasedEmailBackend


class EmailBackend(MailTrailBase, FileBasedEmailBackend):
    BACKEND = 'FILEBASED'

    def send_messages(self, email_messages):
        for message in email_messages:
            self.save_message(message)

        return super(EmailBackend, self).send_messages(email_messages)
