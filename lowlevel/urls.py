from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("alarm/create/", views.AlarmCreateView.as_view(), name="alarm-create"),
    path("alarm/<int:pk>/", views.AlarmDetailView.as_view(), name="alarm-detail"),
    path(
        "alarm/update/<int:pk>/", views.AlarmUpdateView.as_view(), name="alarm-update"
    ),
    path(
        "alarm/delete/<int:pk>/", views.AlarmDeleteView.as_view(), name="alarm-delete"
    ),
    path(
        "alarm/toggle/<int:pk>/", views.AlarmToggleView.as_view(), name="alarm-toggle"
    ),
    # API functions
    path("show_color", views.ColorView.as_view(), name="color"),
    path(
        "transition_color", views.TransitionColorView.as_view(), name="transition_color"
    ),
    path("show_clock", views.ClockView.as_view(), name="clock"),
    path(
        "execute_wake_up_scripts", views.WakeUpLightView.as_view(), name="wake-up-light"
    ),
    path(
        "execute_wake_up_story", views.WakeUpStoryView.as_view(), name="wake-up-story"
    ),
]
