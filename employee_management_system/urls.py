"""employee_management_system URL Configuration."""
from django.contrib import admin
from django.urls import path

from employee_management_system.views import hello_world

urlpatterns = [
    path("admin/", admin.site.urls),
    path("hello/", hello_world),
]
