"""cs350 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import re_path, path, include
from rest_framework import routers
from majorizer import views

from majorizer.views import home_view, register_view

api = routers.DefaultRouter()
api.register('schedules', views.ScheduleViewSet)
api.register('courses', views.CourseViewSet)
api.register('offerings', views.CourseOfferingViewSet)
api.register('students', views.StudentViewSet)

urlpatterns = [
    path('', home_view, name='home'),
    path('api/', include(api.urls)),
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('register/', register_view, name='register'),
]
