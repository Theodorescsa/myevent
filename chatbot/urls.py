from django.urls import path, include

from . import views
app_name = "chatbot"
urlpatterns = [
    path('',views.chatbot,name='chatbot'),
    path('<int:id>/',views.chatbotitem,name='chatbotitem')
    
]
