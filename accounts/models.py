from django.conf import settings
from django.db import models
from django.contrib.auth.models import UserManager, AbstractUser
from django.utils.datetime_safe import datetime

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

    verified_email = models.BooleanField(default=False)

    objects = MyUserManager()


class Token(models.Model):
    name = models.CharField(max_length=20)
    expiry_date = models.DateTimeField()

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return 'id:{} user_id:{} name:{}'.format(self.id, self.user_id, self.name)
