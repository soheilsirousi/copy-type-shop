from django.urls import path
from user.views import LoginView, RegisterView, ProfileView, LogoutView, UserDetailView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('detail/', UserDetailView.as_view(), name='detail'),
]