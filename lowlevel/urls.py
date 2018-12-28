from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('show_color', views.ColorView.as_view(), name='color'),
    path('transition_color', views.TransitionColorView.as_view(), name='transition_color'),
    path('show_clock', views.ClockView.as_view(), name='clock'),
]