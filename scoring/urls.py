from django.urls import path
from . import views

urlpatterns = [
    path('', views.application_form, name='application_form'),
    path('accepted/', views.accepted_applications, name='accepted_applications'),
    path('rejected/', views.rejected_applications, name='rejected_applications'),
    path('delete/<int:pk>/', views.delete_application, name='delete_application'),
]
