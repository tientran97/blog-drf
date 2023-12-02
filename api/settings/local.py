from .base import *  # noqa
from .base import env

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="wfjeiAycshdffrZqrGem5FFhA33U0cbGePEOQmNQRualaqnGdkE",
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

CSRF_TRUSTED_ORIGINS = ["http://localhost:8080"]

EMAIL_BACKEND = "djcelery_email_backends.CeleryEmailBackend"
EMAIL_HOST = env("EMAIL_HOST", default="mailhog")
EMAIL_HOST = env("EMAIL_PORT")
DEFAULT_FORM_EMAIL = "tien.minhtran615@gmail.com"
DOMAIN = env("DOMAIN")
SITE_NAME = "Tien Tran"
