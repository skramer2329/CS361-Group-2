from django.contrib import admin
from .models import Instructor, Ta, Supervisor, Course, Section

# Register your models here.
admin.site.register(Instructor)
admin.site.register(Ta)
admin.site.register(Supervisor)
admin.site.register(Course)
admin.site.register(Section)