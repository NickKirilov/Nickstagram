from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from nickstagram.web.views import IndexView, SearchView

urlpatterns = [
    path('', IndexView.as_view(), name='home page'),

    path('search/', SearchView.as_view(), name='search page')


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
