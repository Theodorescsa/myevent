from django.contrib import admin
from django.urls import path, include
from . import views
app_name = "home"
urlpatterns = [
    path('', views.main,name = "main"),
    path('list_events/', views.list_events,name = "list_events"),
    path('add/', views.add,name = "add"),  
    path('edit/<int:id>/', views.edit,name = "edit"),  
    path('delete/<int:id>/', views.delete,name = "delete"),  
    
    path('test/', views.test,name = "test"),  
    
    path('detail_event/<int:id>/', views.detail,name = "detail"),  
    path("subcribe/<int:id>/",views.subcribe2,name='subcribe2'),
    path("subcribed/",views.didsubcribed,name='subcribed'),
    path("unsubcribe/<int:id>/",views.unsubcribe,name='unsubcribe'),
    path("createroom/<int:id>/", views.index, name="index"),
    path("<str:room_name>/", views.room, name="room"),

      
    
]
