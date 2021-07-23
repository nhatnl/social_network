from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager
from social_network_api import settings

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, null=False, blank= False)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField(null=False, blank=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','age']

    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.email
    
    def __repr__(self) -> str:
        return self.email
