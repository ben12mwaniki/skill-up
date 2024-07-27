from django.db import models

# Create your models here.

class Skill(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
   # image = models.ImageField(upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Student(models.Model):
    name = models.CharField(max_length=100) 
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    skills = models.ManyToManyField(Skill)
    created_at = models.DateTimeField(auto_now_add=True)    

    def __str__(self):
        return self.name        
    
