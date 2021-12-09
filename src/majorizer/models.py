from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db.models.fields import CharField
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


class DBDepartment(models.Model):
    name = models.CharField(max_length=64)


class DBCourse(models.Model):
    course_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=64)
    course_number = models.CharField(max_length=8, unique=True)
    equiv_attr = models.SmallIntegerField(blank=True, null=True)
    prereqs = models.ManyToManyField("DBCourse", symmetrical=False)


class DBCourseOffering(models.Model):
    term = models.CharField(max_length=6)
    instructor = models.CharField(max_length=64)
    start_time = models.TimeField()
    end_time = models.TimeField()
    days = CharField(max_length=9)  # Comma separated list
    room = models.CharField(max_length=8)
    section_num = models.SmallIntegerField()
    course_id = models.ForeignKey(DBCourse, models.DO_NOTHING)


class DBDegreeProgram(models.Model):
    name = models.CharField(max_length=64, default="Unspecified Name")
    is_major = models.BooleanField()
    department_id = models.ForeignKey(DBDepartment, models.DO_NOTHING)
    courses = models.ManyToManyField(DBCourse)


class DBStudent(models.Model):
    name = models.CharField(max_length=64)
    grad_term = models.CharField(max_length=6)
    degrees = models.ManyToManyField(DBDegreeProgram)

class DBSchedule(models.Model):
    name = models.CharField(max_length=64)
    student_id = models.ForeignKey(DBStudent, models.DO_NOTHING)
    courses = models.ManyToManyField(DBCourseOffering)
    is_fall_semester = models.BooleanField(default=True)
    year = models.IntegerField(default=0)


class DBAdvisor(models.Model):
    name = models.CharField(max_length=64)
    department_id = models.ForeignKey(DBDepartment, models.DO_NOTHING)
    shared_schedules = models.ManyToManyField(DBSchedule)


class DBAdvisorCode(models.Model):
    advisor_id = models.ForeignKey(DBAdvisor, models.DO_NOTHING)


class DBComment(models.Model):
    message = models.TextField()
    schedule_id = models.ForeignKey(DBSchedule, models.DO_NOTHING)
    parent_id = models.ForeignKey('self', models.DO_NOTHING)


class DBUser(models.Model):
    user = models.OneToOneField(User, models.CASCADE)
    student_id = models.ForeignKey(DBStudent, models.DO_NOTHING, blank=True, null=True)
    advisor_id = models.ForeignKey(DBAdvisor, models.DO_NOTHING, blank=True, null=True)

'''
@receiver(post_save, sender=DBUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        DBUser.objects.create(user=instance)


@receiver(post_save, sender=DBUser)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
'''