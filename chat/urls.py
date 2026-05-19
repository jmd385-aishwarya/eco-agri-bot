from django.urls import path
from . import views

urlpatterns = [
    # This loads the web interface when you go to http://127.0.0.1:8000/chat/
    path('', views.index, name='index'), 
    
    # This is the hidden URL your frontend JavaScript will send messages to
    path('api/chat/', views.chat_view, name='chat_view'), 
]