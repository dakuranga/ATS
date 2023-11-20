# signuplogin/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.management import call_command
from .models import Team
from django.contrib.auth.signals import user_logged_out
import logging

logger = logging.getLogger(__name__)



@receiver(post_save, sender=Team)
def create_team_database(sender, instance, created, **kwargs):
    if created:
        call_command('create_team_database', domain=instance.domain)


from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

@receiver(user_logged_in)
def set_tenant_on_login(sender, request, user, **kwargs):
    # Set the tenant information in the session
    user_tenant = user.get_team_database()
    request.session['tenant'] = user_tenant
    logger.debug(f"Tenant set on login for user {user.email}: {user_tenant}")

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from settingsapp.models import TenantUser

@receiver(post_save, sender=User)
def create_or_update_tenant_user(sender, instance, created, **kwargs):
    if instance.team:
        tenant_db = instance.get_team_database()

        # Create or update TenantUser in the tenant database
        tenant_user_defaults = {
            'first_name': instance.first_name,
            'last_name': instance.last_name,
            'is_active': instance.is_active,
            'is_verified': instance.is_verified,
            # Add other fields as necessary
        }
        TenantUser.objects.using(tenant_db).update_or_create(
            email=instance.email, 
            defaults=tenant_user_defaults
        )

from django.db.models.signals import post_delete

@receiver(post_delete, sender=User)
def delete_tenant_user(sender, instance, **kwargs):
    if instance.team:
        tenant_db = instance.get_team_database()
        TenantUser.objects.using(tenant_db).filter(email=instance.email).delete()
