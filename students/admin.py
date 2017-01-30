from django.contrib import admin
from .models import Student, Group

# Register your models here.


class GroupInline(admin.StackedInline):
    model = Student

class GroupAdmin(admin.ModelAdmin):
    inlines = [
        GroupInline,
    ]

admin.site.register(Student)
admin.site.register(Group, GroupAdmin)