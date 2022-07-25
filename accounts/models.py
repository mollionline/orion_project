from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    email = models.EmailField(max_length=255, blank=False, verbose_name="Email")
    description = models.CharField(max_length=150, verbose_name='Описание', null=True, blank=True)
