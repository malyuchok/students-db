# -*- coding: utf-8 -*-

from django.db import models

# Create your models here.

class Student(models.Model):

        class Meta(object):
            verbose_name = u"Студент"
            verbose_name_plural = u"Студенти"

        first_name = models.CharField(
            max_length=256,
            blank=False,
            verbose_name=u"Name")

        last_name = models.CharField(
            max_length=256,
            blank=False,
            verbose_name=u"Прізвище")

        middle_name = models.CharField(
            max_length=256,
            blank=False,
            verbose_name=u"По-батькові",
            default=''
            )

        student_group = models.ForeignKey('Group',
            verbose_name=u"Група",
            blank=False,
            null=True,
            on_delete=models.PROTECT
            )


        birthday = models.DateField(
            blank=False,
            verbose_name=u"Дата народження",
            null=True
            )

        ticket = models.CharField(
            max_length=256,
            blank=False,
            verbose_name=u"Білет"
            )
        def __unicode__(self):
                return u"%s %s" % (self.first_name, self.last_name)

        notes = models.TextField(
            blank=True,
            verbose_name=u"Додаткові нотатки"
            )

class Group(models.Model):

    class Meta(object):
        verbose_name = u"Група"
        verbose_name_plural = u"Групи"

    title = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u"Назва"
        )

    def __unicode__(self):
        return u"%s" % (self.title,)

    leader = models.OneToOneField('Student',
        verbose_name=u"Староста",
        blank=True,
        null=True,
        on_delete=models.SET_NULL
        )


