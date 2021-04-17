from django.db import models

# Create your models here.

class User(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    address = models.CharField(max_length=40)
    email = models.EmailField(max_length=30)


class Course(models.Model):
    name = models.CharField(max_length=20)
    course_number = models.IntegerField()
    instructor = models.ForeignKey(User)
    ta_list = []
