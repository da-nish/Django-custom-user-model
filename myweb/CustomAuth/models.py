# users/models.py
import datetime
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class manage(BaseUserManager):
    def create_user(self, name, user_type, email, password=None):
        if not email:
            raise ValueError("no email")
        user = self.model(
            email=self.normalize_email(email),
        )

        user.name = name
        user.user_type = user_type
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            name="CustomAdmin",
            user_type="Admin",#set any type
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    email = models.EmailField(verbose_name='email', unique=True, max_length=60)
    name = models.CharField(max_length=60, default="no-name")
    user_type = models.CharField(max_length=60, default="local")

    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = manage()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

