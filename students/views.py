# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import UpdateView, DeleteView
from .models import Student, Group
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# Create your views here.

class StudentUpdateView(UpdateView):
    model = Student
    template_name = 'students/students_edit.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse('home')
    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(reverse('home'))
        else:
            return super(StudentUpdateView, self).post(request, *args, **kwargs)

class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'students/confirm_delete.html'

    def get_success_url(self):
        return reverse('home')

class GroupDeleteView(DeleteView):
    model = Group
    template_name = 'students/group_confirm_delete.html'

    def get_success_url(self):
        return reverse('groups_list')

class GroupUpdateView(UpdateView):
    model = Group
    template_name = 'students/groups_edit.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse('groups_list')
    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(reverse('groups_list'))
        else:
            return super(GroupUpdateView, self).post(request, *args, **kwargs)

def students_list(request):
    students = Student.objects.all()

    order_by = request.GET.get('order_by', '')
    if order_by in ('last_name', 'first_name', 'ticket'):
        students = students.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            students = students.reverse()

    paginator = Paginator(students, 10)
    page = request.GET.get('page')
    try:
        students = paginator.page(page)
    except PageNotAnInteger:
        students = paginator.page(1)
    except EmptyPage:
        students = paginator.page(paginator.num_pages)

    return render(request, 'students/students_list.html', {'students': students})

def students_add(request):
    if request.method == "POST":
        if request.POST.get('add_button') is not None:
            errors = {}
            data = {'middle_name':request.POST.get('middle_name'),
                    'notes':request.POST.get('notes')}
            first_name = request.POST.get('first_name', '').strip()
            if not first_name:
                errors['first_name'] = u"Ім'я є обов'язковим"
            else:
                data['first_name'] = first_name
            last_name = request.POST.get('last_name', '').strip()
            if not last_name:
                errors['last_name'] = u"Прізвище є обов'язковим"
            else:
                data['last_name'] = last_name
            birthday = request.POST.get('birthday', '').strip()
            if not birthday:
                errors['birthday'] = u"Дата народження є обов'язковою"
            else:
                data['birthday'] = birthday
            ticket = request.POST.get('ticket', '').strip()
            if not ticket:
                errors['ticket'] = u"Номер білета є обов'язковим"
            else:
                data['ticket'] = ticket
            student_group = request.POST.get('student_group', '').strip()
            if not student_group:
                errors['student_group'] = u"Оберіть групу для студента"
            else:
                data['student_group'] = Group.objects.get(pk=student_group)
            if not errors:
                student = Student(**data)
                student.save()
                return HttpResponseRedirect(reverse('home'))
            else:
                return render(request, 'students/students_add.html',
                              {'groups': Group.objects.all().order_by('title'),
                               'errors': errors})
        elif request.POST.get('cancel_button') is not None:
            return HttpResponseRedirect(reverse('home'))
    else:
        return render(request, 'students/students_add.html',
                      {'groups': Group.objects.all().order_by('title')})

def students_edit(request, sid):
    return HttpResponse('<h1>Stud edit blyat</h1>' .format(sid))

def students_delete(request, sid):
    return HttpResponse('<h1>Stud delete blyat</h1>' .format(sid))

def groups_list(request):
    groups = Group.objects.all()
    return render(request, 'students/groups_list.html', {'groups': groups})

def groups_add(request):
    if request.method == "POST":
        if request.POST.get('add_button') is not None:
            errors = {}
            data = {}
            title = request.POST.get('title', '').strip()
            if not title:
                errors['title'] = u"Group name is required"
            else:
                data['title'] = title
            leader = request.POST.get('leader', '').strip()
            if not leader:
                errors['leader'] = u"Leader is required"
            else:
                data['leader'] = Student.objects.get(pk=leader)
            if not errors:
                group = Group(**data)
                group.save()
                return HttpResponseRedirect(reverse('groups_list'))
            else:
                return render(request, 'students/groups_add.html',
                              {'groups': Student.objects.all(),
                               'errors': errors})
        elif request.POST.get('cancel_button') is not None:
            return HttpResponseRedirect(reverse('groups_list'))
    else:
        return render(request, 'students/groups_add.html',
                      {'students': Student.objects.all()})

def groups_edit(request, sid):
    return HttpResponse('<h1> groyp edit</h1>' .format(sid))

def groups_delete(request, sid):
    return HttpResponse('<h1> groyp delete</h1>' .format(sid))

def groups_students(request, sid):
    student = Student.objects.all().filter(student_group=sid)
    group = Group.objects.all()
    return render(request, 'students/groups_students.html' .format(sid), {'students': student}, {'group': group})