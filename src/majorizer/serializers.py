from majorizer.models import *
from rest_framework import serializers


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DBSchedule
        fields = ["name", "student_id", "courses"]
        depth = 2


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = DBCourse
        fields = ["name", "course_number", "equiv_attr"]


class CourseOfferingSerializer(serializers.ModelSerializer):
    class Meta:
        model = DBCourseOffering
        fields = ["term", "instructor", "start_time", "end_time", "days", "room", "section_num", "course_id"]
        depth = 1


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DBStudent
        fields = ["name", "grad_term", "degrees"]
        depth = 2
