from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser, UserManager


class ChefManager(UserManager):
    pass
    
class ChefIdentity(AbstractUser):
    objects = ChefManager()
