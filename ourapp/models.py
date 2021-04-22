from django.db import models
import abc
#from .models import Instructor, Supervisor, Ta, Section, Course
# Create your models here.



class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)

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
    name = models.CharField(max_length=15)
    number = models.IntegerField()
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    #ta_list = models.ManyToOneRel(Ta)
    time = models.DateTimeField()


class Section(models.Model):
   # course = models.ForeignKey(Course)
    number = models.IntegerField()





