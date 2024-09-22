from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('home/signout', views.signout, name='signout'),
    path('home/', views.home, name='home'),
    path('home/home', views.home, name='home'),

    path('register_patient/', views.register_patient, name='register_patient'),
    path('register_patient/patient_details', views.patient_details, name='patient_detials'),
    path('register_patient/home', views.home, name='home'),


    path('patient_details', views.patient_details, name='patient_details'),
    path('home/patient_details', views.patient_details, name='patient_details'),

    path('show_searched_patient', views.show_searched_patient, name='show_searched_patient'),
    path('show_searched_patient_for_remove_patient', views.show_searched_patient_for_remove_patient, name='show_searched_patient_for_remove_patient'),

    path('save_treatment_details', views.save_treatment_details, name='save_treatment_details'),
    path('home/show_searched_patient', views.show_searched_patient, name='show_searched_patient'),
    path('home/show_searched_patient_for_remove_patient', views.show_searched_patient_for_remove_patient, name='show_searched_patient_for_remove_patient'),

    path('remove_patient', views.remove_patient, name='remove_patient'),
    path('home/remove_patient', views.remove_patient, name='remove_patient'),


    path('remove_patient_from_db', views.remove_patient_from_db, name='remove_patient_from_db'),
    path('home/remove_patient_from_db', views.remove_patient_from_db, name='remove_patient_from_db'),

    path('change_patient_details', views.change_patient_details, name='change_patient_details'),

    path('change_treatment_details', views.change_treatment_details, name='change_treatment_details'),

    path('change_treatment_details_in_db', views.change_treatment_details_in_db, name='change_treatment_details_in_db')
]