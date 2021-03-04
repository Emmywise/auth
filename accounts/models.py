from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from django.db import models
#from .create import CustomUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.base_user import BaseUserManager
from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework_simplejwt.authentication import JWTAuthentication

class UserManager(BaseUserManager):
#Custom user model manager where email is the unique identifiersfor authentication instead of usernames.

    def create_user(self, email, password, username, **extra_fields):

        if username is None:
            raise TypeError('input username')
        if email is None:
            raise TypeError('input email')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    # def create_user(self, email, password=None, **extra_fields):
    #     extra_fields.setdefault('is_superuser', False)
    #     return self._create_user(email, password, **extra_fields)

    # def create_superuser(self, email, password, **extra_fields):
    #     extra_fields.setdefault('is_superuser', True)

    #     if extra_fields.get('is_superuser') is not True:
    #         raise ValueError('Superuser must have is_superuser=True.')

    #     return self.create_user(email, password, **extra_fields) 
    def create_superuser(self,  email, username, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        user = self.create_user(username, email, password, **extra_fields)
        user.username=username
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    #user = models.OneToOneField(User,on_delete=models.CASCADE)
    username = models.CharField(max_length=225, unique=True, db_index=True)
    email = models.EmailField(max_length=225, unique=True, db_index=True)
    is_verified = models.BooleanField(default= False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()
    
    def __str__(self):
        return self.email

    def tokens(self):
        refresh=RefreshToken.for_user(self)



        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

    