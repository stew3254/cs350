# Generated by Django 3.2.9 on 2021-11-22 01:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Advisor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('courseID', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64)),
                ('courseNumber', models.CharField(max_length=8, unique=True)),
                ('equivAttr', models.SmallIntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CourseOffering',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('term', models.CharField(max_length=6)),
                ('instructor', models.CharField(max_length=64)),
                ('time', models.TimeField()),
                ('room', models.CharField(max_length=8)),
                ('sectionNum', models.SmallIntegerField()),
                ('courseID', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='majorizer.course')),
            ],
        ),
        migrations.CreateModel(
            name='DegreeProgram',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isMajor', models.BooleanField()),
                ('courses', models.ManyToManyField(to='majorizer.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('username', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('password', models.BinaryField(max_length=60)),
                ('token', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('gradTerm', models.CharField(max_length=6)),
                ('degrees', models.ManyToManyField(to='majorizer.DegreeProgram')),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('courses', models.ManyToManyField(to='majorizer.CourseOffering')),
                ('studentID', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='majorizer.student')),
            ],
        ),
        migrations.AddField(
            model_name='degreeprogram',
            name='departmentID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='majorizer.department'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('parentID', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='majorizer.comment')),
                ('scheduleID', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='majorizer.schedule')),
            ],
        ),
        migrations.CreateModel(
            name='AdvisorCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('advisorID', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='majorizer.advisor')),
            ],
        ),
        migrations.AddField(
            model_name='advisor',
            name='departmentID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='majorizer.department'),
        ),
        migrations.AddField(
            model_name='advisor',
            name='sharedSchedules',
            field=models.ManyToManyField(to='majorizer.Schedule'),
        ),
    ]
