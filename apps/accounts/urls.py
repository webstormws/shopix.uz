from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, MyTokenObtainPairView, ProfileView, SavedCardListCreateView, SavedCardDeleteView, UserListView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("users/", UserListView.as_view(), name="users-list"),
    path("login/", MyTokenObtainPairView.as_view(), name="login"),          # login -> access + refresh token
    path("login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("cards/", SavedCardListCreateView.as_view(), name="cards"),
    path("cards/<int:pk>/", SavedCardDeleteView.as_view(), name="card-delete"),
]
