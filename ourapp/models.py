from django.db import models
import abc
from .models import Instructor, Supervisor, Ta, Section, Course
# Create your models here.



class User(models.Model):
    first_name = models.CharField()
    last_name = models.CharField()
    password = models.CharField()
    address = models.CharField()
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)

    class Meta:
        abstract=True


class Instructor(User):
    courses = models.ManyToOneRel(Course)
    sections = models.ManyToOneRel(Section)


class Supervisor(User):
    pass


class Ta(User):
    courses = models.ManyToManyField(Course)
    sections = models.ManyToOneRel(Section)


class Course(models.Model):
    name = models.CharField()
    number = models.IntegerField()
    instructor = models.ForeignKey(Instructor)
    ta_list = models.ManyToOneRel(Ta)
    time = models.DateTimeField()


class Section(models.Model):
    course = models.ForeignKey(Course)
    number = models.IntegerField()





