from django.db import models
from signuplogin.models import User
from django.db import models

class TenantUser(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    def __str__(self):
        return self.email
    
class UserEmail(models.Model):
    user = models.OneToOneField(TenantUser, on_delete=models.CASCADE)
    email_address = models.CharField(max_length=200, null=True, blank=True)
    access_token = models.CharField(max_length=200)  # Store the OAuth access token
    refresh_token = models.CharField(max_length=200, blank=True, null=True)  # Store the OAuth refresh token (if available)
    token_expiration = models.DateTimeField(null=True, blank=True)
    email_provider = models.CharField(max_length=100, null=True, blank=True) 

    def __str__(self):
        return self.email_address

from django.db import models
from ckeditor.fields import RichTextField
from attachments.models import Attachment
from django.conf import settings 

class EmailTemplate(models.Model):
    name = models.CharField(max_length=255, unique=True)
    subject = models.CharField(max_length=255)
    body = RichTextField()

    def __str__(self):
        return self.name

class TemplateAttachment(Attachment):
    template = models.ForeignKey(EmailTemplate, on_delete=models.CASCADE)

class EmailSignature(models.Model):
    user = models.OneToOneField(TenantUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    content = RichTextField()

