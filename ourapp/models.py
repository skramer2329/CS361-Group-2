from django.db import models
import abc
#from .models import Instructor, Supervisor, Ta, Section, Course

# Create your models here.


class MyUser(models.Model):
    first_name = models.CharField(max_length=100, default=None)
    last_name = models.CharField(max_length=100, default=None)
    password = models.CharField(max_length=100, default=None)
    address = models.CharField(max_length=100, default=None)
    email = models.EmailField(default=None)
    phone_number = models.CharField(max_length=15, default=None)

    role = models.CharField(max_length=10, default=None)

    def __str__(self):
        return self.first_name


"""class Instructor(User):
    courses = models.ManyToOneRel(Course)
    sections = models.ManyToOneRel(Section)
    pass


class Supervisor(User):
    pass


class Ta(User):
    courses = models.ManyToManyField(Course)
    sections = models.ManyToOneRel(Section)
    pass"""


class MyCourse(models.Model):
    name = models.CharField(max_length=15, default=None)
    number = models.IntegerField(default=None)
    instructor = models.ForeignKey(MyUser(role='instructor'),on_delete=models.CASCADE,default=None)
    #ta_list = models.ManyToOneRel(MyUser)
    #time = models.DateTimeField()


class Section(models.Model):
    course = models.ForeignKey(MyCourse, on_delete=models.CASCADE, default=None)
    number = models.IntegerField(default=None)







