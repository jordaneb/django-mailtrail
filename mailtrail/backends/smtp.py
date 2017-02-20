from mailtrail.backends.base import MailTrailBase
from django.core.mail.backends.smtp import EmailBackend as SMTPEmailBackend


class EmailBackend(MailTrailBase, SMTPEmailBackend):
    """
    Send emails using an SMTP server - as simple as that.

    REPLACES: django.core.mail.backends.smtp.EmailBackend
    """
    BACKEND = 'SMTP'

    def send_messages(self, email_messages):
        for message in email_messages:
            self.save_message(message)

        return super(EmailBackend, self).send_messages(email_messages)
