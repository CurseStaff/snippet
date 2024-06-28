from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("", views.snippet_filter_list, name="snippet_filter_list"),
    path("snippet/<int:pk>/", views.snippet_detail, name="snippet_detail"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("signup/", views.signup, name="signup"),
    path("home/", views.home, name="home"),
    path("profile/", views.profile, name="profile"),
    path("profile/<str:username>/", views.update_profile, name="edit_profile"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("generate/", views.generate_snippet, name="generate_snippet"),
]
