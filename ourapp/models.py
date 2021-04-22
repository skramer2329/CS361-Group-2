from django.db import models
import abc
#from .models import Instructor, Supervisor, Ta, Section, Course

# Create your models here.


class User(models.Model):
    first_name = models.CharField(max_length=100, default=None)
    last_name = models.CharField(max_length=100, default=None)
    password = models.CharField(max_length=100, default=None)
    address = models.CharField(max_length=100, default=None)
    email = models.EmailField(default=None)
    phone_number = models.CharField(max_length=15, default=None)

    class Meta:
        abstract=True

class Instructor(User):
#    courses = models.ManyToOneRel(Course)
#    sections = models.ManyToOneRel(Section)
    pass


class Supervisor(User):
    pass


class Ta(User):
#    courses = models.ManyToManyField(Course)
#    sections = models.ManyToOneRel(Section)
    pass

class Course(models.Model):
    name = models.CharField(max_length=15, default=None)
    number = models.IntegerField(default=None)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, default=None)
    #ta_list = models.ManyToOneRel(Ta)
    #time = models.DateTimeField()



class Section(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, default=None)
    number = models.IntegerField(default=None)






