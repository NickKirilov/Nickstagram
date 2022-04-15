from django.contrib.auth.views import LogoutView
from django.urls import path

from nickstagram.accounts.views import UserLoginView, RegisterView, ProfileMoreInfo, EditProfileView, CreateProfileView, \
    DeleteProfileView, ChangePasswordView, ForgottenPasswordView

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login page'),
    path('register/', RegisterView.as_view(), name='register page'),
    path('profile/<int:pk>/', ProfileMoreInfo.as_view(), name='profile page'),
    path('profile/edit/<int:pk>/', EditProfileView.as_view(), name='edit profile page'),
    path('profile/logout/<int:pk>/', LogoutView.as_view(), name='logout page'),
    path('profile/create/', CreateProfileView.as_view(), name='create profile page'),
    path('profile/delete/<int:pk>/', DeleteProfileView.as_view(), name='delete profile page'),
    path('reset-password/<int:pk>/', ChangePasswordView.as_view(), name='edit password page'),
    path('send-password/', ForgottenPasswordView.as_view(), name='send password')
]