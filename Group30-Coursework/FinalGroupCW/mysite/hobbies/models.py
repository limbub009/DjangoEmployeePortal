from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth import authenticate, login
from django.utils.translation import ugettext_lazy as _
# Create your models here.


#HOBBY
class Hobby(models.Model):
    name = models.CharField(max_length=50)
    def to_dict(self):
        """Method for converting hobby attributes to a dictionary"""
        return {
            'id': self.id,
            'name': self.name,
        }

    def __str__(self):
        return f"{self.name}"


#USER
class extendedUser(BaseUserManager):
    # required method for BaseUserManager
    def create_user(self, username, password, email, city, dob):
        email = self.normalize_email(email)
        user = self.model(
            username = username,
            email = email,
            dob = dob,
            city = city,
            is_staff = True,
            is_superuser = True,
            is_admin = True,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, email, city, dob):
        return self.create_user(username, password, email, city, dob)



class User(AbstractUser):
    #define them again
    username = models.CharField(max_length=50, unique = True)
    password = models.CharField(max_length=200)
    email = models.EmailField(max_length = 250)
    dob = models.DateField()
    city = models.CharField(max_length=50)
    profile_pic = models.ImageField(default='default.jpg', null=True, blank=True)
    hobbies = models.ManyToManyField(Hobby, blank=True, related_name = "user")
    is_admin = models.BooleanField(default = False)
    is_superuser = models.BooleanField(default = False)
    is_staff = models.BooleanField(default = False)

    objects = extendedUser()

    USERNAME_FIELD = 'username'

    # # this refers to required fields for creating a superuser
    REQUIRED_FIELDS = ["city", "email", "dob"]

    def to_dict(self):
        """Method for converting user attributes to a dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'dob': self.dob,
            'city': self.city,
            'hobbies': [ hobby.id for hobby in self.hobbies.all() ],
            'api': reverse('update_user_api', kwargs={'id': self.id}),
            'send_fr': reverse('send_friend_api', kwargs={'id': self.id}),
            'profile_pic': self.profile_pic.url,
        }
# Friend Request
class FriendRequest(models.Model):
    sender = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='receiver', on_delete=models.CASCADE)
    are_friends = models.BooleanField(default=False)

    def __str__(self):
        return f" {self.sender}, {self.receiver}"
    # JSON Dictionary
    def to_dict(self):
        """Method for converting model attributes to a dictionary"""
        return {
            'id': self.id,
            'sender': self.sender,
            'receiver': self.receiver,
            'are_friends': self.are_friends,
        }
