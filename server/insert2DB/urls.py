from django.urls import path
from . import views

urlpatterns = [
    #Path for getting all data inputs
    path('', views.index, name='index'),

    #Path for getting data from single school
    path('single/<str:schoolName>/<str:departmentName>/', views.singleData, name = 'singleData'),
    
    #Path for uploading data
    path('upload/', views.uploadData, name = 'uploadData'),
    
    #Path for sending data to the oracle
    path('oracle/', views.testOracle, name = 'testOracle'),
]
