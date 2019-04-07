from django.db import models
from django.contrib.auth.models import UserManager, AbstractUser

from turnthepage.constants import USERNAME, EMAIL, PASSWORD


class MyUserManager(UserManager):
    def create_user(self, username=None, email=None, password=None, **extra_fields):
        if not (username and email):
            raise ValueError('Users must have an email address and username')
        return super().create_user(username=username, email=email, password=password, **extra_fields)

    def create_test_user(self, **extra_fields):
        return super().create_user(username=USERNAME, email=EMAIL, password=PASSWORD, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    objects = MyUserManager()
