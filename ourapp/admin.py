from django.contrib import admin
from .models import  Course, Section, MyUser

# Register your models here.

admin.site.register(Course)
admin.site.register(MyUser)
admin.site.register(Section)