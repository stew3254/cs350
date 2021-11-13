from django.db import models


# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=64)


class User(models.Model):
    username = models.CharField(max_length=32, primary_key=True)
    password = models.BinaryField(max_length=60)
    token = models.CharField(max_length=64)


class Student(models.Model):
    name = models.CharField(max_length=64)
    gradTerm = models.CharField(max_length=6)


class Advisor(models.Model):
    name = models.CharField(max_length=64)
    departmentID = models.ForeignKey(Department, models.CASCADE)


class AdvisorCode(models.Model):
    advisorID = models.ForeignKey(Advisor, models.CASCADE)
