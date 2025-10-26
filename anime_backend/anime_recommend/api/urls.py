# api/urls.py
from django.urls import path
from .views import (
    RegisterUserView, CustomTokenObtainPairView, UserDetailView,
    LogoutView, UpdateUserView, ChangePasswordView,
    AnimeListView, AnimeDetailView, AddAnimeView, DeleteAnimeView, 
    UserWatchListView, AddWatchHistoryView, RecommendForUserView
)

urlpatterns = [
    path("register/", RegisterUserView.as_view(), name="register"),
    path("login/", CustomTokenObtainPairView.as_view(), name="login"),
    path("user/", UserDetailView.as_view(), name="user_detail"),
    path("user/update/", UpdateUserView.as_view(), name="update_user"),
    path("change-password/", ChangePasswordView.as_view(), name="change_password"),
    path("logout/", LogoutView.as_view(), name="logout"),

    # Anime APIs
    path("anime/", AnimeListView.as_view(), name="anime_list"),
    path("anime/<int:pk>/", AnimeDetailView.as_view(), name="anime_detail"),
    path("anime/add/", AddAnimeView.as_view(), name="add_anime"),
    path("anime/<int:pk>/delete/", DeleteAnimeView.as_view(), name="delete_anime"), 

    # User Watch History APIs
    path("user/watchlist/", UserWatchListView.as_view(), name="user_watchlist"),
    path("user/watchlist/add/<int:anime_id>/", AddWatchHistoryView.as_view(), name="add_watch_history"),
    path("recommend/", RecommendForUserView.as_view(), name="recommend_user"),
]
