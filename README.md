# Django MailTrail
A seamless integration that makes Django email awesome.

## Installation
MailTrail is designed to work seamlessly with existing and new projects - all you have to do use the MailTrail backends.

Make sure that you add `mailtrail` to your `INSTALLED_APPS` like so:
```python
INSTALLED_APPS = [
    ...
    
    'mailtrail',
]
```

Now change the `EMAIL_BACKEND` variable in your `settings.py` to one of the available backends:

##### Console

The equivalent of Django's built-in console backend.
```python
EMAIL_BACKEND = 'mailtrail.backends.console.EmailBackend'
```

##### Database

A custom backend that saves emails in the database but doesn't send them; useful for debugging.
```python
EMAIL_BACKEND = 'mailtrail.backends.database.EmailBackend'
```

##### Console

The equivalent of Django's built-in console backend.
```python
EMAIL_BACKEND = 'mailtrail.backends.console.EmailBackend'
```

##### File Based

The equivalent of Django's built-in filebased backend.
```python
EMAIL_BACKEND = 'mailtrail.backends.filebased.EmailBackend'
```

##### SMTP

The equivalent of Django's built-in SMTP backend.
```python
EMAIL_BACKEND = 'mailtrail.backends.smtp.EmailBackend'
```

Finally, run migrations with `python manage.py migrate` to prepare your database for MailTrail.

## Usage
All emails sent with `django.core.mail` will now be stored in your database and are accessible
in the Django Admin!
