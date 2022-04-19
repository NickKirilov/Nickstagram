from django.contrib.auth.views import LogoutView
from django.urls import path

from nickstagram.accounts.views import UserLoginView, RegisterView, ProfileMoreInfo, EditProfileView, CreateProfileView, \
    DeleteProfileView

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login page'),
    path('register/', RegisterView.as_view(), name='register page'),
    path('profile/', ProfileMoreInfo.as_view(), name='profile page'),
    path('profile/edit/', EditProfileView.as_view(), name='edit profile page'),
    path('profile/logout/', LogoutView.as_view(), name='logout page'),
    path('profile/create/', CreateProfileView.as_view(), name='create profile page'),
    path('profile/delete/', DeleteProfileView.as_view(), name='delete profile page'),
]