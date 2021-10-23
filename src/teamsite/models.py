from django.db import models

# Create your models here.
class Report(models.Model):
    title = models.CharField(max_length = 100, default="Weekly Report")
    date = models.DateField()
    text = models.TextField()