from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from nickstagram.web.views import IndexView, CreatePostView, PostDetailsView, EditPostView, DeletePostView, SearchView

urlpatterns = [
    path('', IndexView.as_view(), name='home page'),

    path('post/create/', CreatePostView.as_view(), name='create post page'),
    path('post/details/<int:pk>/', PostDetailsView.as_view(), name='post details page'),
    path('post/edit/<int:pk>/', EditPostView.as_view(), name='post edit page'),
    path('post/delete/<int:pk>', DeletePostView.as_view(), name='post delete page'),

    path('search/', SearchView.as_view(), name='search page')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


