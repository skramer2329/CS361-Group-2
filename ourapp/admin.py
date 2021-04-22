from django.contrib import admin
from .models import  MyCourse, Section, MyUser

# Register your models here.

admin.site.register(MyCourse)
admin.site.register(MyUser)
admin.site.register(Section)