from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField


# Model linked to the User model
# This model will store the user's profile information
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.TextField()
    saved_resources = ArrayField(models.TextField())
    created_resources = ArrayField(models.TextField())

    def __str__(self):  
        return self.user.username
     


