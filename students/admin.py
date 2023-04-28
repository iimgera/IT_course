from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Student, 
    Flow, 
    Direction,
    User
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'email',
        'password',
    )


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'first_name',
        'last_name',
        'age',
        'direction'
    )
        

@admin.register(Flow)
class FlowAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title'
    )


@admin.register(Direction)
class DirectionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'flow'
    )