from django.urls import path

from . import views

urlpatterns = [
    path("discover/", views.discover, name="discover"),
    path("like/<str:username>/", views.like_profile, name="like_profile"),
    path("pass/<str:username>/", views.pass_profile, name="pass_profile"),
    path("matches/", views.matches_list, name="matches_list"),
]
