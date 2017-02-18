from mailtrail.models import Email, get_recipient_model


class MailTrailBase:
    BLANK = ''

    def save_message(self, message):
        """
        Save a sent message in the database
        """
        Recipient = get_recipient_model()

        email = Email.objects.create(
            subject=message.subject,
            message=message.message(),
            from_email=message.from_email,
            html_message=getattr(message, 'html_message', self.BLANK)
        )

        for recipient_email in message.recipients():
            # Create recipients if they do not exist and
            recipient = Recipient.objects.get_or_create(email=recipient_email)[0]
            email.recipients.add(recipient)
