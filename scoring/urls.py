from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('form/', views.application_form, name='application_form'),
    path('accepted/', views.accepted_applications, name='accepted_applications'),
    path('rejected/', views.rejected_applications, name='rejected_applications'),
    path('pending/', views.pending_applications, name='pending_applications'),
    path('process/', views.process_applications, name='process_applications'),
    path('portfolio/', views.optimal_portfolio, name='optimal_portfolio'),
    path('portfolio/remove/<int:pk>/', views.remove_from_portfolio, name='remove_from_portfolio'),
    path('delete/<int:pk>/', views.delete_application, name='delete_application'),
]
