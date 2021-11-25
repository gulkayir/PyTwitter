from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django_countries.data import COUNTRIES
from django.db.models import Q, F


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.create_activation_code()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    username = None
    email = models.EmailField(max_length=100, primary_key=True)
    avatar = models.ImageField(upload_to='uploads/avatar', blank=True, null=True)
    header = models.ImageField(upload_to='uploads/headers', blank=True, null=True)
    about = models.CharField(max_length=160, blank=True, null=True)
    country = models.CharField(max_length=30,choices=sorted(COUNTRIES.items()), null=True, blank=True)
    is_active = models.BooleanField(default=False)
    created_date = models.DateField(auto_now_add=True)
    # followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followers', blank=True)
    # followings = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followings', blank=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    activation_code = models.CharField(max_length=255, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return f'{self.username}'

    def create_activation_code(self):
        import hashlib
        string = self.email + self.email
        encode_string = string.encode()
        md5_object = hashlib.md5(encode_string)
        activation_code = md5_object.hexdigest()
        self.activation_code = activation_code

# class Following(models.Model):
#     user = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
#     following_user = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    # class Meta:
    #     constraints = [
#             models.UniqueConstraint(fields=['user', 'following_user'],
#                                     name='unique_followers'),
#             models.CheckConstraint(check=Q(user_id=F('following_user_id')),
#                                    name='self_not_follow')
#         ]
#
#     def __str__(self):
#         return f'{self.user_id} follows {self.following_user_id}'
#
