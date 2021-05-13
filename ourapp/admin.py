from django.contrib import admin
from .models import  MyCourse, MySection, MyUser, Skill

# Register your models here.

admin.site.register(MyCourse)
admin.site.register(MyUser)
admin.site.register(MySection)
admin.site.register(Skill)