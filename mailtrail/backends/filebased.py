from mailtrail.backends.base import MailTrailBase
from django.core.mail.backends.filebased import EmailBackend as FileBasedEmailBackend


class EmailBackend(MailTrailBase, FileBasedEmailBackend):
    """
    Create a file with the contents of the email. Requires `settings.EMAIL_FILE_PATH`
    to be defined.

    REPLACES: django.core.mail.backends.filebased.EmailBackend
    """
    BACKEND = 'FILEBASED'

    def send_messages(self, email_messages):
        for message in email_messages:
            self.save_message(message)

        return super(EmailBackend, self).send_messages(email_messages)
