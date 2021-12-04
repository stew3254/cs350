import json

from majorizer.models import *
from datetime import time

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Imports test data into the database'

    def handle(self, *args, **kwargs):
        try:
            if kwargs["name"] is not None:
                import_data(kwargs["name"])
        except:
            raise CommandError('Initalization failed.')


def test_data():
    test_department = DBDepartment(name="Test Department")
    test_department.save()

    test_course = DBCourse(course_id=1234, name="Test Course", course_number="TEST1234")
    test_course.save()

    test_course_offering = DBCourseOffering(term="F21", instructor="Professor McTeacherson", start_time=time(11),
                                            end_time=time(12, 30), days="0,2,4", room="bathroom", section_num=1,
                                            course_id=test_course)
    test_course_offering.save()

    test_degree_program = DBDegreeProgram(is_major=True, department_id=test_department)
    test_degree_program.save()
    test_degree_program.courses.add(test_course)

    test_student = DBStudent(name="Test Student", grad_term="F2023")
    test_student.save()
    test_student.degrees.add(test_degree_program)

    test_schedule = DBSchedule(name="Test Schedule", student_id=test_student)
    test_schedule.save()
    test_schedule.courses.add(test_course_offering)


def import_data(name=None):
    if name is None:
        test_data()
    else:
        data = json.loads(open(name, "r").read())
        # TODO implement this function
