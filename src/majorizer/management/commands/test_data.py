import json

from majorizer.models import *
from majorizer.util import parse, new_parse, create_user
from datetime import time

import traceback

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Imports test data into the database'

    def handle(self, *args, **kwargs):
        try:
            import_data("cs_classes.csv")
            import_data("chem_e_classes.csv")
            test_data()
        except Exception as e:
            traceback.print_exc()
            raise CommandError(f'Initalization failed due to error: {e}')


def test_data():
    cs_department, _ = DBDepartment.objects.get_or_create(name="Computer Science")

    test_course, _ = DBCourse.objects.get_or_create(course_id=1234, name="Test Course", course_number="TEST1234")
    test_course2, _ = DBCourse.objects.get_or_create(course_id=4321, name="Test Course 2", course_number="TEST4321")
    test_course3, _ = DBCourse.objects.get_or_create(course_id=1010, name="Test Course 3", course_number="TEST1010")
    test_course.prereqs.add(test_course2)
    test_course.prereqs.add(test_course3)

    cs_degree, _ = DBDegreeProgram.objects.get_or_create(name="Computer Science", is_major=True, department_id=cs_department)
    core_cs_classes = ["CS141", "CS142", "CS241", "CS242", "CS341", "CS344", "CS345", "CS350", "CS444"]
    #cs_electives = DBCourse.objects.exclude(course_number__in=core_cs_classes)
    cs_degree.courses.add(*(DBCourse.objects.filter(course_number__in=core_cs_classes)))
    #cs_degree.courses.add(*cs_electives)

    cheme_degree, _ = DBDegreeProgram.objects.get_or_create(name="Chemical Engineering", is_major=True, department_id=cs_department)
    core_cheme_classes = ["CH210", "CH220", "CH260", "CH320", "CH330", "CH350", "CH360", "CH370", "CH410", "CH420", "CH460"]
    cheme_degree.courses.add(*(DBCourse.objects.filter(course_number__in=core_cheme_classes)))


    test_degree, _ = DBDegreeProgram.objects.get_or_create(name="Test Major", is_major=True, department_id=cs_department)
    test_degree.courses.add(test_course)

    test_degree2, _ = DBDegreeProgram.objects.get_or_create(name="Test Minor", is_major=False, department_id=cs_department)
    test_degree.courses.add(test_course)

    #create_user("Test", "test", "test", "Sp", "2026", test_degree.id)

    test_offering, _ = DBCourseOffering.objects.get_or_create(term="F21", instructor="Professor McTeacherson", start_time=time(11),
                                            end_time=time(12, 30), days="0,2,4", room="bathroom", section_num=1,
                                            course_id=test_course)
    test_offering3, _ = DBCourseOffering.objects.get_or_create(term="F21", instructor="Professor McTeacherson", start_time=time(9),
                                            end_time=time(10, 30), days="0,1,2", room="bathroom", section_num=2,
                                            course_id=test_course3)
    test_offering2, _ = DBCourseOffering.objects.get_or_create(term="F21", instructor="Professor McTeacherson", start_time=time(14),
                                            end_time=time(15, 30), days="1,3", room="bathroom", section_num=1,
                                            course_id=test_course2)

    #test_student, _ = DBStudent.objects.get_or_create(name="Test Student", grad_term="F2023")
    #test_student.degrees.add(test_degree)

    #test_schedule, _ = DBSchedule.objects.get_or_create(name="Test Schedule", student_id=test_student)
    #test_schedule.courses.add(test_offering)


def import_data(name=None):
    test_data()
    if name is not None:
        new_parse(name)
