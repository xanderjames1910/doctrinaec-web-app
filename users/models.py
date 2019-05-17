from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# class User(auth.models.User, auth.models.PermissionsMixin):

#     def __str__(self):
#         return '@{}'.format(self.username)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=250, blank=True)
    birth_date = models.DateTimeField(null=True, blank=True)
    career = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'
