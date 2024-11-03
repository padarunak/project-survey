from django.contrib import admin

from .models import *

class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'color')



admin.site.register(Subject, SubjectAdmin)


# Register your models here.
