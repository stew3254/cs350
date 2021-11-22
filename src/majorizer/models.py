from django.db import models


# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=64)


class Course(models.Model):
    courseID = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=64)
    courseNumber = models.CharField(max_length=8, unique=True)
    equivAttr = models.SmallIntegerField(null=True)


class CourseOffering(models.Model):
    term = models.CharField(max_length=6)
    instructor = models.CharField(max_length=64)
    time = models.TimeField()
    room = models.CharField(max_length=8)
    sectionNum = models.SmallIntegerField()
    courseID = models.ForeignKey(Course, models.DO_NOTHING)


class DegreeProgram(models.Model):
    isMajor = models.BooleanField()
    departmentID = models.ForeignKey(Department, models.DO_NOTHING)
    courses = models.ManyToManyField(Course)


class User(models.Model):
    username = models.CharField(max_length=32, primary_key=True)
    password = models.BinaryField(max_length=60)
    token = models.CharField(max_length=64)


class Student(models.Model):
    name = models.CharField(max_length=64)
    gradTerm = models.CharField(max_length=6)
    degrees = models.ManyToManyField(DegreeProgram)


class Schedule(models.Model):
    name = models.CharField(max_length=64)
    studentID = models.ForeignKey(Student, models.DO_NOTHING)
    courses = models.ManyToManyField(CourseOffering)


class Advisor(models.Model):
    name = models.CharField(max_length=64)
    departmentID = models.ForeignKey(Department, models.DO_NOTHING)
    sharedSchedules = models.ManyToManyField(Schedule)


class AdvisorCode(models.Model):
    advisorID = models.ForeignKey(Advisor, models.DO_NOTHING)


class Comment(models.Model):
    message = models.TextField()
    scheduleID = models.ForeignKey(Schedule, models.DO_NOTHING)
    parentID = models.ForeignKey('self', models.DO_NOTHING)
