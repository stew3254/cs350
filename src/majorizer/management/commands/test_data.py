import json

from majorizer.models import *
from datetime import time

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Imports test data into the database'

    def handle(self, *args, **kwargs):
        try:
            import_data(name=kwargs.get("name"))
        except Exception as e:
            raise CommandError(f'Initalization failed due to error: {e}')


def test_data():
    test_department, _ = DBDepartment.objects.get_or_create(name="Test Department")

    test_course, _ = DBCourse.objects.get_or_create(course_id=1234, name="Test Course", course_number="TEST1234")

    test_offering, _ = DBCourseOffering.objects.get_or_create(term="F21", instructor="Professor McTeacherson",
                                                              start_time=time(11),
                                                              end_time=time(12, 30), days="0,2,4", room="bathroom",
                                                              section_num=1,
                                                              course_id=test_course)

    test_degree, _ = DBDegreeProgram.objects.get_or_create(is_major=True, department_id=test_department)
    test_degree.courses.add(test_course)

    test_student, _ = DBStudent.objects.get_or_create(name="Test Student", grad_term="F2023")
    test_student.degrees.add(test_degree)

    test_schedule, _ = DBSchedule.objects.get_or_create(name="Test Schedule", student_id=test_student)
    test_schedule.courses.add(test_offering)


def import_data(name=None):
    if name is None:
        test_data()
    else:
        data = json.loads(open(name, "r").read())
        # TODO implement this function
