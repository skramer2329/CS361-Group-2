from django.db import models
import abc

# Create your models here.


class Account(abc):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    address = models.CharField(max_length=40)
    email = models.EmailField(max_length=30)
    phone_number = models.CharField(max_length=15)


class Course(models.Model):
    name = models.CharField(max_length=20)
    course_number = models.IntegerField()
    instructor = models.ForeignKey(Account)
    ta_list = models.ManyToManyField(Account)
    time = models.DateTimeField()


class Section(models.Model):
    course = models.ForeignKey(Course)


class Supervisor(Account):
    pass


class Instructor(Account):
    courses = models.ManyToOneRel(Course)
    sections = models.ManyToOneRel(Section)


class Ta(Account):
    courses = models.ManyToManyField(Course)
    sections = models.ManyToOneRel(Section)
