from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Department)
admin.site.register(User)
admin.site.register(Student)
admin.site.register(Advisor)
admin.site.register(AdvisorCode)
