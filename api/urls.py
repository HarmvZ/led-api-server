from django.urls import path
from api import views

urlpatterns = [
    path('base/', views.base_view),
    path('set_color/', views.set_color),
    path('transition_color/', views.transition_color),
]