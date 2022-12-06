from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class Usuarios(AbstractUser):
    username = models.CharField(max_length=50, blank=True, null=True, unique=True)
    email = models.EmailField(_('email address'), unique=True)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
