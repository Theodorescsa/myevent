from django.urls import path, include

from . import views
app_name = "signin"
urlpatterns = [
    path("",views.signin,name='signin'),
    
]
