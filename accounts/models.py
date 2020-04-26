from datetime import timedelta
from django.conf import settings
from django.shortcuts import reverse
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)

from django.core.mail import send_mail
from django.template.loader import get_template
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, email="cfast@gmail.com", username=None, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")
        user_obj = self.model(
            email = self.normalize_email(email),
            username=username
        )
        user_obj.set_password(password) # change user password
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.is_active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email="cfast@gmail.com",username=None, password=None):
        user = self.create_user(
                email,
                username=username,
                password=password,
                is_staff=True
        )
        return user

    def create_superuser(self, email="cfast@gmail.com", username=None, password=None):
        user = self.create_user(
                email,
                username=username,
                password=password,
                is_staff=True,
                is_admin=True
        )
        return user


class User(AbstractBaseUser):
    email       = models.EmailField(max_length=255, blank=True,null=True)
    username   = models.CharField(max_length=255,blank=True,null=True,unique=True) #username
    is_active   = models.BooleanField(default=True,blank=True,null=True) # can login
    staff       = models.BooleanField(default=False) # staff user non superuser
    admin       = models.BooleanField(default=False) # superuser
    # password = models.CharField(max_length=200)
    # password2 = models.CharField(max_length=200)


    USERNAME_FIELD = 'username' #username
    # USERNAME_FIELD and password are required by default
    REQUIRED_FIELDS = [] #['full_name'] #python manage.py createsuperuser

    objects = UserManager()

    def __str__(self):
        return self.username

    def get_full_name(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        if self.is_admin:
            return True
        return self.staff

    @property
    def is_admin(self):
        return self.admin

class login_page(models.Model):
    email = models.EmailField(null=True,blank=True)
    username = models.CharField(max_length=50,blank=True,null=True,unique=True)
    password = models.CharField(max_length=200)






