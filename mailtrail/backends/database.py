from mailtrail.backends.base import MailTrailBase


class EmailBackend(MailTrailBase):
    """
    Store email in the database and don't send anything. Useful
    for debugging.
    """
    BACKEND = 'DATABASE'

    def __init__(self, *args, **kwargs):
        pass

    def send_messages(self, email_messages):
        for message in email_messages:
            self.save_message(message)
