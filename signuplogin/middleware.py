import logging
from .thread_local import set_current_request

logger = logging.getLogger(__name__)

class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        set_current_request(request)

        # Retrieve tenant from session
        request.tenant = request.session.get('tenant')
        if request.tenant:
            logger.debug(f"Middleware's Tenant: {request.tenant}")
        else:
            logger.debug("Middleware says No Tenant")

        response = self.get_response(request)
        return response
