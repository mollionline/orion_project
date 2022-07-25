from django.contrib.auth.models import AbstractUser
from django.db import models
MODERATOR_STATUS_CHOICES = (
    ('Not Customer', 'Not Customer'),
    ('Customer', 'Customer'),
)


# Create your models here.
class User(AbstractUser):
    email = models.EmailField(max_length=255, blank=False, verbose_name="Email")
    description = models.CharField(max_length=150, verbose_name='Описание', null=True, blank=True)
    user_permission = models.CharField(max_length=50, null=False, blank=False,
                                       choices=MODERATOR_STATUS_CHOICES, verbose_name="Права устройства",
                                       default='Not Customer')
