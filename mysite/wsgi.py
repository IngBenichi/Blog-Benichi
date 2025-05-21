"""
WSGI config for mysite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
import subprocess
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

# Ejecutar collectstatic si se define una variable de entorno
if os.environ.get("RUN_COLLECTSTATIC", "false").lower() == "true":
    try:
        print("==> Ejecutando collectstatic en Vercel...")
        subprocess.run(["python3", "manage.py", "collectstatic", "--noinput"], check=True)
        print("==> collectstatic ejecutado exitosamente.")
    except subprocess.CalledProcessError as e:
        print("==> Error al ejecutar collectstatic:", e)


application = get_wsgi_application()

# Para compatibilidad con Vercel
app = application