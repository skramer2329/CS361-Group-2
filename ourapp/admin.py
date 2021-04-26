from django.contrib import admin
from .models import  MyCourse, SectionOne, MyUser, Joke

# Register your models here.

admin.site.register(MyCourse)
admin.site.register(MyUser)
admin.site.register(SectionOne)
admin.site.register(Joke)