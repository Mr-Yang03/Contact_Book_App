from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_contact, name='create_contact'),
    path('update/<int:contact_id>/', views.update_contact, name='update_contact'),
    path('delete/<int:contact_id>/', views.delete_contact, name='delete_contact'),
]