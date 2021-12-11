from django.shortcuts import render, redirect
from majorizer.models import *
from majorizer.util import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from rest_framework import viewsets
from rest_framework import permissions
from .forms import ClassSearchForm, LoginForm
from .serializers import *
from datetime import time
from django.http import HttpResponse


timeslots = []
init_timeslots(timeslots)

# Create your views here.
def home_view(request):
    login_form = LoginForm()
    class_search_form = ClassSearchForm()

    django_user = request.user
    logged_in = django_user.is_authenticated
        
    if logged_in:
        majorizer_user = DBUser.objects.get(user=django_user)
        schedules = DBSchedule.objects.filter(student_id=majorizer_user.student_id)
        if schedules:
            if "selected_schedule_id" in request.session:
                active_schedule = DBSchedule.objects.get(id=request.session['selected_schedule_id'])
            else:
                active_schedule = schedules[0]
        else:
            active_schedule = None
    else:
        active_schedule = None
        schedules = None

    if active_schedule is not None:
        schedule_to_timeslots(active_schedule, timeslots)

    name = ""
    class_search_term = ""
    class_search_results = []
    offerings = None
    selected_class = None


    context_dict = {}

    # Handle forms
    if request.method == 'POST':
        if "login_button" in request.POST:
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                name = login_form.cleaned_data['username']
                pword = login_form.cleaned_data['password']
                django_user = authenticate(username=name, password=pword)
                if django_user is not None:
                    login(request, django_user)
                    logged_in = True
                    majorizer_user = DBUser.objects.get(user=django_user)
                    schedules = DBSchedule.objects.filter(student_id=majorizer_user.student_id)
                else:
                    print("\nno such user!\n")
                    logged_in = False
                
                if schedules:
                    if "selected_schedule_id" in request.session:
                        active_schedule = DBSchedule.objects.get(id=request.session['selected_schedule_id'])
                    else:
                        active_schedule = schedules[0]
                else:
                    active_schedule = None
                

        elif "logout_button" in request.POST:
            logout(request)
            logged_in = False
            schedules = None

        elif "class_search_button" in request.POST:
            class_search_form = ClassSearchForm(request.POST)
            if class_search_form.is_valid():
                class_search_term = class_search_form.cleaned_data['search_term']
                class_search_results = search_classes(class_search_term)

        elif "class_search_result_button" in request.POST:
            # print(request.POST['class_search_result_button'])
            selected_class = request.POST['class_search_result_button']
            offerings = get_course_offerings(selected_class, active_schedule)

        elif "remove_course_from_schedule_button" in request.POST:
            course_to_remove = request.POST["remove_course_from_schedule_button"]
            remove_course_from_schedule(course_to_remove, active_schedule)
            schedule_to_timeslots(active_schedule, timeslots)

        elif "course_offering_button" in request.POST:
            course_offering_to_add = request.POST['course_offering_button']
            course = DBCourseOffering.objects.get(pk=course_offering_to_add).course_id

            course_offering_message = validate_prerequisites_met(course, majorizer_user.student_id, active_schedule)
            print(course_offering_message)
            if not course_offering_message:
                add_course_to_schedule(course_offering_to_add, active_schedule)
                schedule_to_timeslots(active_schedule, timeslots)
            else:
                context_dict['course_offering_message'] = course_offering_message

        elif "new_schedule_button" in request.POST:
            new_schedule_name = request.POST['new_schedule_name']
            new_schedule_semester = True if request.POST['new_schedule_semester'] == 'F' else False
            new_schedule_year = request.POST['new_schedule_year']

            new_schedule_message = validate_new_schedule(new_schedule_name, new_schedule_semester, new_schedule_year, majorizer_user.student_id)
            
            if not new_schedule_message:
                new_schedule, _ = DBSchedule.objects.get_or_create(name=new_schedule_name, student_id=majorizer_user.student_id,
                                                                is_fall_semester = new_schedule_semester, year = new_schedule_year)

                schedules = DBSchedule.objects.filter(student_id=majorizer_user.student_id)
                active_schedule = new_schedule
                request.session['selected_schedule_id'] = active_schedule.id
            else:
                context_dict['new_schedule_message'] = new_schedule_message

        elif "schedule_select_button" in request.POST:
            selected_schedule = request.POST['schedules']
            active_schedule = DBSchedule.objects.get(id=selected_schedule)
            request.session['selected_schedule_id'] = active_schedule.id
            schedule_to_timeslots(active_schedule, timeslots)

        elif "schedule_delete_button" in request.POST:
            active_schedule.delete()
            if "selected_schedule_id" in request.session:
                request.session.pop('selected_schedule_id')
            schedules = DBSchedule.objects.filter(student_id=majorizer_user.student_id)
            if schedules:
                active_schedule = schedules.first()
                request.session['selected_schedule_id'] = active_schedule.id

    context_dict['current_page'] = 'home'
    context_dict['login_form'] = login_form
    context_dict['class_search_form'] = class_search_form
    context_dict['timeslots'] = timeslots
    context_dict['class_search_term'] = class_search_term
    context_dict['class_search_results'] = class_search_results
    context_dict['logged_in'] = logged_in
    context_dict['offerings'] = offerings
    context_dict['selected_class'] = selected_class
    context_dict['active_schedule'] = active_schedule
    context_dict['schedules'] = schedules

    return render(request, "home.html", context_dict)


def register_view(request):
    context_dict = {}

    registration_form = LoginForm()
    login_form = LoginForm()

    # Handle forms
    if request.method == 'POST':
        uname = request.POST['username']
        pword = request.POST['password']
        full_name = request.POST['name']
        grad_semester = request.POST['grad_semester']
        grad_year = request.POST['grad_year']

        degree_programs = request.POST.getlist('degree_programs')

        #TODO: Validate username and password

        create_user(full_name, uname, pword, grad_semester, grad_year, degree_programs)

        return redirect("/")

    context_dict['current_page'] = 'register'
    context_dict['registration_form'] = registration_form
    context_dict['login_form'] = login_form
    context_dict['majors'] = get_majors()
    context_dict['minors'] = get_minors()

    return render(request, "register.html", context_dict)
  
def profile_view(request):
    logged_in = request.user.is_authenticated

    if logged_in:
        django_user = request.user
        majorizer_user = DBUser.objects.get(user = django_user)
        student = majorizer_user.student_id
        degrees = student.degrees.all()
        schedules = DBSchedule.objects.filter(student_id = student)

    context_dict = {}
    context_dict['current_page'] = 'profile'
    context_dict['logged_in'] = logged_in
    context_dict['student'] = student
    context_dict['degrees'] = degrees
    context_dict['schedules'] = schedules

    return render(request, "profile.html", context_dict)

class ScheduleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = DBSchedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]


class CourseViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = DBCourse.objects.all()
    serializer_class = CourseSerializer
    # permission_classes = [permissions.IsAuthenticated]


class CourseOfferingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = DBCourseOffering.objects.all()
    serializer_class = CourseOfferingSerializer
    # permission_classes = [permissions.IsAuthenticated]


class StudentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = DBStudent.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]
