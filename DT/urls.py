"""
URL configuration for DT project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.landingpage, name="landingPage"),
    path('homepage/', views.homepage, name="homepage"),
    path('homepage/ ', views.landingpage, name="landingpage"),
    path('homepage/saved-timetables', views.saved_timetables, name="saved_timetables"),
    path('table/', views.table),
    path('lecture/', views.lecture, name='lecture'),   
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('login/signup', views.signup, name='signup'),
    path('signup/login', views.login, name='login'),
    path('logout', views.logout_page, name="logout"),
    path('save-timetable/', views.save_timetable, name='save_timetable'),
    path('saved-timetables/', views.saved_timetables, name='saved_timetables'),
    path('view-timetable/<int:timetable_id>/', views.view_saved_timetable, name='view_saved_timetable'),
   
]
