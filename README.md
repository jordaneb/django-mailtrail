# Django MailTrail
A seamless integration that makes Django email awesome.

## Installation
MailTrail is designed to work seamlessly with existing and new projects - all you have to do use the MailTrail backends.

```
pip install django-mailtrail
```

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

For example, an email send with `django.core.mail.send_mail()` will look a little like this:

**Viewing an email**
![screen shot 2017-02-20 at 13 20 28](https://cloud.githubusercontent.com/assets/20087139/23126647/b251fec6-f76f-11e6-8d13-0b36f6451ede.png)

**Viewing an email's raw payload**
![screen shot 2017-02-20 at 13 23 10](https://cloud.githubusercontent.com/assets/20087139/23126689/df772ff2-f76f-11e6-8b72-6369330384d4.png)

**Resending an email**
![screen shot 2017-02-20 at 13 23 34](https://cloud.githubusercontent.com/assets/20087139/23126691/e0d2061a-f76f-11e6-9e9f-f9df0333ccf3.png)

**Forwarding an email**
![screen shot 2017-02-20 at 13 23 56](https://cloud.githubusercontent.com/assets/20087139/23126694/e259a0f6-f76f-11e6-9397-df8dede5be2d.png)

