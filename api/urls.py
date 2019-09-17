from django.urls import path
from api import views

urlpatterns = [
    path('base/', views.base_view),
    path('set_color/', views.set_color),
    path('transition_color/', views.transition_color),
    path('show_clock/', views.show_clock),
    path('show_animation/', views.show_animation),
]