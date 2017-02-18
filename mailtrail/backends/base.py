from mailtrail.models import Email, get_recipient_model


class MailTrailBase:
    BLANK = ''
    BACKEND = None

    def save_message(self, message):
        """
        Save a sent message in the database
        """
        Recipient = get_recipient_model()

        # Uses email library to parse messages
        payload = message.message().get_payload()

        # Determine whether message has a HTML version or not
        plaintext = payload[0].get_payload() if not isinstance(payload[0], str) else payload
        html = payload[1].get_payload() if not isinstance(payload[1], str) else payload

        email = Email.objects.create(
            subject=message.subject,
            payload=message.message(),
            plaintext_message=plaintext,
            html_message=html,
            from_email=message.from_email,
            backend=self.BACKEND
        )

        for recipient_email in message.recipients():
            # Create recipients if they do not exist and
            recipient = Recipient.objects.get_or_create(email=recipient_email)[0]
            email.recipients.add(recipient)
