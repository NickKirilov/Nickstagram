from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path
from django.views.static import serve

from nickstagram.web.views import IndexView, CreatePostView, PostDetailsView, EditPostView, DeletePostView

urlpatterns = [
    path('', IndexView.as_view(), name='home page'),

    path('post/create/', CreatePostView.as_view(), name='create post page'),
    path('post/details/<int:pk>/', PostDetailsView.as_view(), name='post details page'),
    path('post/edit/<int:pk>/', EditPostView.as_view(), name='post edit page'),
    path('post/delete/<int:pk>', DeletePostView.as_view(), name='post delete page'),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


