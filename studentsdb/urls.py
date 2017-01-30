"""studentsdb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from students.views import students_list, students_add, students_edit, students_delete, groups_list, groups_add, groups_students, StudentUpdateView, StudentDeleteView, GroupDeleteView, GroupUpdateView

urlpatterns = [

    url(r'^$', students_list, name="home"),

    url(r'students/add/$', students_add, name="students_add"),

    url(r'students/(?P<pk>\d+)/edit/$', StudentUpdateView.as_view(), name="students_edit"),

    url(r'students/(?P<pk>\d+)/delete/$', StudentDeleteView.as_view(), name="students_delete"),

    url(r'groups/$', groups_list, name="groups_list"),

    url(r'groups/(?P<sid>\d+)/all/$', groups_students, name="groups_students"),

    url(r'groups/add/$', groups_add, name="groups_add"),

    url(r'groups/(?P<pk>\d+)/delete/$', GroupDeleteView.as_view(), name="groups_delete"),

    url(r'groups/(?P<pk>\d+)/edit/$', GroupUpdateView.as_view(), name="groups_edit"),

    url(r'^admin/', include(admin.site.urls)),
]
