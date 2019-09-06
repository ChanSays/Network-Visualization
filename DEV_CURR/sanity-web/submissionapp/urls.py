from django.urls import path, re_path, include
from . import views

urlpatterns = [
    path('', views.submit_job, name='submit_job'),
    re_path(r'^django-pam/', include('django_pam.urls')),
]
