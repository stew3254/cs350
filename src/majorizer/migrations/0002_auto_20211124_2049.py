# Generated by Django 3.2 on 2021-11-25 01:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('majorizer', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Advisor',
            new_name='DBAdvisor',
        ),
        migrations.RenameModel(
            old_name='AdvisorCode',
            new_name='DBAdvisorCode',
        ),
        migrations.RenameModel(
            old_name='Comment',
            new_name='DBComment',
        ),
        migrations.RenameModel(
            old_name='Course',
            new_name='DBCourse',
        ),
        migrations.RenameModel(
            old_name='CourseOffering',
            new_name='DBCourseOffering',
        ),
        migrations.RenameModel(
            old_name='DegreeProgram',
            new_name='DBDegreeProgram',
        ),
        migrations.RenameModel(
            old_name='Department',
            new_name='DBDepartment',
        ),
        migrations.RenameModel(
            old_name='Schedule',
            new_name='DBSchedule',
        ),
        migrations.RenameModel(
            old_name='Student',
            new_name='DBStudent',
        ),
        migrations.DeleteModel(
            name='User',
        ),
        migrations.RenameField(
            model_name='dbadvisor',
            old_name='departmentID',
            new_name='department_id',
        ),
        migrations.RenameField(
            model_name='dbadvisorcode',
            old_name='advisorID',
            new_name='advisor_id',
        ),
        migrations.RenameField(
            model_name='dbcomment',
            old_name='parentID',
            new_name='parent_id',
        ),
        migrations.RenameField(
            model_name='dbcomment',
            old_name='scheduleID',
            new_name='schedule_id',
        ),
        migrations.RenameField(
            model_name='dbcourse',
            old_name='courseID',
            new_name='course_id',
        ),
        migrations.RenameField(
            model_name='dbcourse',
            old_name='courseNumber',
            new_name='course_number',
        ),
        migrations.RenameField(
            model_name='dbcourse',
            old_name='equivAttr',
            new_name='equiv_attr',
        ),
        migrations.RenameField(
            model_name='dbcourseoffering',
            old_name='courseID',
            new_name='course_id',
        ),
        migrations.RenameField(
            model_name='dbcourseoffering',
            old_name='sectionNum',
            new_name='section_num',
        ),
        migrations.RenameField(
            model_name='dbdegreeprogram',
            old_name='departmentID',
            new_name='department_id',
        ),
        migrations.RenameField(
            model_name='dbdegreeprogram',
            old_name='isMajor',
            new_name='is_major',
        ),
        migrations.RenameField(
            model_name='dbschedule',
            old_name='studentID',
            new_name='student_id',
        ),
        migrations.RenameField(
            model_name='dbstudent',
            old_name='gradTerm',
            new_name='grad_term',
        ),
        migrations.RemoveField(
            model_name='dbadvisor',
            name='sharedSchedules',
        ),
        migrations.AddField(
            model_name='dbadvisor',
            name='shared_schedules',
            field=models.ManyToManyField(to='majorizer.DBSchedule'),
        ),
    ]