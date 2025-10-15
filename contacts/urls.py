from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_contact, name='create_contact'),
    path('update/<int:contact_id>/', views.update_contact, name='update_contact'),
    path('delete/<int:contact_id>/', views.delete_contact, name='delete_contact'),
    path('groups/', views.groups, name='groups'),
    path('groups/create/', views.create_group, name='create_group'),
    path('groups/update/<int:group_id>/', views.update_group, name='update_group'),
    path('groups/delete/<int:group_id>/', views.delete_group, name='delete_group'),
]