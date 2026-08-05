from django.urls import path
from soat import views

urlpatterns = [
    path('',views.index,name="index"),
    path('procesar',views.procesar,name="procesar"),
]
