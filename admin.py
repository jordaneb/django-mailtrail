from django.contrib import admin
from models import Email, get_recipient_model

admin.site.register(Email)
admin.site.register(get_recipient_model())
