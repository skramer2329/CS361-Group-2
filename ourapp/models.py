from django.db import models
import abc

# Create your models here.


class MyUser(models.Model):
    first_name = models.CharField(max_length=100, default=None)
    last_name = models.CharField(max_length=100, default=None)
    password = models.CharField(max_length=100, default=None)
    address = models.CharField(max_length=100, default=None)
    email = models.EmailField(default=None)
    phone_number = models.CharField(max_length=15, default=None)

    role = models.CharField(max_length=10, default=None)

    """def __str__(self):
        pass"""

    def is_ta(self):
        pass

    def is_instructor(self):
        pass

    def is_supervisor(self):
        pass


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
    name = models.CharField(max_length=100, default=None)
    number = models.IntegerField(default=None)
    people = models.ManyToManyField(MyUser, default=None, blank=True)
    #sections = models.ManyToManyField(Section, default=None, blank=True)
    #instructor = models.ForeignKey(MyUser, blank=True, on_delete=models.CASCADE)


class Joke(models.Model):
    #var2 = models.ForeignKey(MyCourse, on_delete=models.CASCADE, default=None)
    var = models.ForeignKey(MyUser, on_delete=models.CASCADE, default=None)


class SectionOne(models.Model):
    #course = models.ForeignKey(MyCourse, on_delete=models.CASCADE, default=None)
    #number = models.IntegerField(default=None)
    teacher = models.ForeignKey(MyUser, on_delete=models.CASCADE, default=None)


# Section refers to lab or course section
# We just need to figure out how to put a person in the Section model
"""class Section(models.Model):
    #course = models.ForeignKey(to=MyCourse, on_delete=models.CASCADE, default=None)
    number = models.IntegerField(default=None)
    teacher = models.ForeignKey(MyUser, on_delete=models.CASCADE, default=None)"""




