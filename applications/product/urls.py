from django.urls import path, include
from .routers import router
# from .views import list_media_files


urlpatterns = [
    path("", include(router.urls)),
    # path('list-files/', list_media_files, name='list_media_files'),
]
