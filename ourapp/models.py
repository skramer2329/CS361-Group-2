from django.db import models
import abc

# Create your models here.


class Role(models.TextChoices):
    INSTRUCTOR = 'instructor'
    TA = 'ta'
    SUPERVISOR = 'supervisor'


class MyUser(models.Model):
    first_name = models.CharField(max_length=100, default=None)
    last_name = models.CharField(max_length=100, default=None)
    password = models.CharField(max_length=100, default=None)
    address = models.CharField(max_length=100, default=None)
    email = models.EmailField(default=None)
    phone_number = models.CharField(max_length=15, default=None)

    role = models.CharField(max_length=100, default=None, choices=Role.choices)

    def __str__(self):
        return self.first_name + " " + self.last_name


    def is_ta(self):
        return self.role == 'ta'

    def is_instructor(self):
        return self.role == 'instructor'

    def is_supervisor(self):
        return self.role == 'supervisor'


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


    def __str__(self):
        return self.name



# Section refers to lab or course section
class MySection(models.Model):
    course = models.ForeignKey(MyCourse, on_delete=models.CASCADE, default=None)
    number = models.IntegerField(default=None)
    teacher = models.ForeignKey(MyUser, on_delete=models.CASCADE, default=None, null=True, blank=True)


    def __str__(self):
        return str(self.course.number) + "-" + str(self.number)



# Section refers to lab or course section
# We just need to figure out how to put a person in the Section model
"""class Section(models.Model):
    #course = models.ForeignKey(to=MyCourse, on_delete=models.CASCADE, default=None)
    number = models.IntegerField(default=None)
    teacher = models.ForeignKey(MyUser, on_delete=models.CASCADE, default=None)"""




