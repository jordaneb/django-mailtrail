from mailtrail.backends.base import MailTrailBase


class EmailBackend(MailTrailBase):
    """
    The database backend is very useful for debugging templates and
    maybe for creating internal messaging systems - that's up to you
    to figure out though!
    """
    BACKEND = 'DATABASE'

    def __init__(self, *args, **kwargs):
        pass

    def send_messages(self, email_messages):
        for message in email_messages:
            self.save_message(message)
