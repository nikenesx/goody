from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('add-review/<int:doc_id>/', views.add_review),
    path('review', views.review),
]
