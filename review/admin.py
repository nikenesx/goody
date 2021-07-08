from django.contrib import admin
from review.models import *
from django.db import models

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('doctor_name', 'display_specialty_name')
    search_fields = ('doctor_name', 'specialty__specialty_name')


    @staticmethod
    def display_specialty_name(doctor):
        return ', '.join([specialty.specialty_name for specialty in doctor.specialty.all()])


@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    search_fields = ['specialty_name']
    list_display = ('specialty_name',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('display_review_doctor', 'review_date', 'review_update_date', 'original_rev_text', 'processed_rev_text', 'ip_address', 'user')
    list_filter = ('review_date', 'user')
    search_fields = ['review_doctor__doctor_name', 'review_date', 'ip_address', 'user__username']
    readonly_fields = ('review_date', 'review_update_date', 'processed_rev_text')
    autocomplete_fields = ('review_doctor',)

    @staticmethod
    def display_review_doctor(review):
        return review.review_doctor.doctor_name


@admin.register(CurseWord)
class CurseWordAdmin(admin.ModelAdmin):
    search_fields = ['word']
    list_display = ('word',)


@admin.register(ExceptionWord)
class ExceptionWordAdmin(admin.ModelAdmin):
    search_fields = ['word']
    list_display = ('word',)
