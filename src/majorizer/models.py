from django.db import models


# Create your models here.
class DBDepartment(models.Model):
    name = models.CharField(max_length=64)


class DBCourse(models.Model):
    course_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=64)
    course_number = models.CharField(max_length=8, unique=True)
    equiv_attr = models.SmallIntegerField(null=True)


class DBCourseOffering(models.Model):
    term = models.CharField(max_length=6)
    instructor = models.CharField(max_length=64)
    time = models.TimeField()
    room = models.CharField(max_length=8)
    section_num = models.SmallIntegerField()
    course_id = models.ForeignKey(DBCourse, models.DO_NOTHING)


class DBDegreeProgram(models.Model):
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
