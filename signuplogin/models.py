from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from pathlib import Path
from django.core.management import call_command
from django.db import models

class Team(models.Model):
    domain = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.domain
    
class UserManager(BaseUserManager):

    def _assign_team(self, email):
        domain = email.split('@')[-1]
        team, created = Team.objects.get_or_create(domain=domain)
        return team
    
    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save(using=self._db)
        user.team = self._assign_team(email)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password):
        user = self.create_user(email, first_name, last_name, password)
        user.is_staff = True
        user.is_superuser = True
        user.is_verified = True
        user.is_active = True 
        user.save(using=self._db)
        return user
      
    def send_confirmation_email(self, user, request):
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        mail_subject = 'Complete your Koldboot Signup'
        message = render_to_string('email_confirmation.html', {
            'user': user,
            'domain': get_current_site(request).domain,
            'uid': uid,
            'token': token,
        })
        email = EmailMultiAlternatives(mail_subject, '', to=[user.email])
        email.attach_alternative(message, "text/html")

        email.send()

import logging
from django.db import models

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False) 
    is_staff = models.BooleanField(default=False)
    team = models.ForeignKey(Team, related_name='users', on_delete=models.CASCADE, null=True)

    def get_team_database(self):
        if self.team:
            db_name = f"team_{self.team.domain.replace('.', '_')}"
        else:
            db_name = 'default'
        return db_name

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='',
        related_name="customuser_groups",
        related_query_name="user",
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="customuser_user_permissions",
        related_query_name="user",
    )

    def __str__(self):
        return self.email

