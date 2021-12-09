from majorizer.models import *
from datetime import time


test_department = DBDepartment(name="Test Department")
test_department.save()

test_course = DBCourse(course_id=1234, name="Test Course", course_number="TEST1234")
test_course.save()

test_course_2 = DBCourse(course_id=4321, name="Test Course 2", course_number="TEST4321")
test_course_2.save()


test_course_offering = DBCourseOffering(term="F21", instructor="Professor McTeacherson", start_time = time(11),
end_time = time(13), days="0,2,3,4", room="bathroom", section_num=1, course_id=test_course)
test_course_offering.save()

test_course_offering_2 = DBCourseOffering(term="F21", instructor="Professor McTeacherson", start_time = time(15),
end_time = time(17, 15), days="2, 4", room="bathroom", section_num=1, course_id=test_course_2)
test_course_offering_2.save()

test_degree_program = DBDegreeProgram(is_major=True, department_id=test_department)
test_degree_program.save()
test_degree_program.courses.add(test_course)
test_degree_program.courses.add(test_course_2)

test_student = DBStudent(name="Test Student", grad_term="F2023")
test_student.save()
test_student.degrees.add(test_degree_program)

test_schedule = DBSchedule(name="Test Schedule", student_id=test_student)
test_schedule.save()
test_schedule.courses.add(test_course_offering)
test_schedule.courses.add(test_course_offering_2)