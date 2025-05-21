import logging
import sys

logger = logging.getLogger(__name__)

class RequestLoggerMiddleware:
    """Middleware para registrar todas las peticiones HTTP en tiempo real."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        log_message = f"📥 REQUEST: {request.method} {request.path} - {request.META.get('REMOTE_ADDR')}"
        logger.info(log_message)
        sys.stdout.flush()  # Fuerza la escritura inmediata

        response = self.get_response(request)

        log_message = f"📤 RESPONSE: {response.status_code} {request.path}"
        logger.info(log_message)
        sys.stdout.flush()  # Fuerza la escritura inmediata

        return response
