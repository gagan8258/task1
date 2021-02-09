from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('frequency/', views.frequency),
    path('result/',views.result,name="resultview"),
]
