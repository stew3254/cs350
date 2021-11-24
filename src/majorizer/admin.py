from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Department)
admin.site.register(Course)
admin.site.register(CourseOffering)
admin.site.register(DegreeProgram)
admin.site.register(User)
admin.site.register(Student)
admin.site.register(Schedule)
admin.site.register(Advisor)
admin.site.register(AdvisorCode)
admin.site.register(Comment)
