from django.urls import path

from . import views

urlpatterns = [
    path("<int:match_id>/", views.conversation, name="conversation"),
]
