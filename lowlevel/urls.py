from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('show_clock', views.ClockView.as_view(), name='clock'),
]