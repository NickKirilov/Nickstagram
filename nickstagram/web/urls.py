from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.urls import path
from nickstagram.web.views import IndexView, CreatePostView, PostDetailsView

urlpatterns = [
    path('', IndexView.as_view(), name='home page'),

    path('post/create/', CreatePostView.as_view(), name='create post page'),
    path('post/details/<int:pk>/', PostDetailsView.as_view(), name='post details page'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


