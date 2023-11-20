import logging
from signuplogin.thread_local import get_current_request
from django.conf import settings  


logger = logging.getLogger(__name__)

class TenantDatabaseRouter:
    def db_for_read(self, model, **hints):
        # List of models that should always use the default database for read
        default_read_models = ['user', 'team', 'group', 'permission', 'session']

        # Check if the model is in the default_read_models list
        if model._meta.model_name.lower() in default_read_models:
            return 'default'

        request = get_current_request()
        if request and hasattr(request, 'tenant'):
            tenant_db = request.tenant

            user_model = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

            if (
                model == user_model and
                request.user.is_superuser and
                request.user.email == 'i@i.com'
            ):
                return 'default'
            
            logger.debug(f"Routing DB read for model {model.__name__} to {tenant_db}")
            return tenant_db

        return 'default'

    def db_for_write(self, model, **hints):
        # List of models that should always use the default database for write
        default_write_models = ['user', 'team', 'group', 'permission', 'session']

        # Check if the model is in the default_write_models list
        if model._meta.model_name.lower() in default_write_models:
            return 'default'

        request = get_current_request()
        if request and hasattr(request, 'tenant'):
            tenant_db = request.tenant

            user_model = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

            if (
                model == user_model and
                request.user.is_superuser and
                request.user.email == 'i@i.com'
            ):
                return 'default'
            
            
            
            # Check if the user is a member of the "Admin Team" and route to default database
            if request.user.team and request.user.team.domain == 'i.com':
                return 'default'

            logger.debug(f"Routing DB write for model {model.__name__} to {tenant_db}")
            return tenant_db

        # For non-superusers, use the tenant-specific database
        return 'default'
