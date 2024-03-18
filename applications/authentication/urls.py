from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter

from .views import ProfileUpdateView, ProfileSetView, FileUploadAPIView, download_file, UserViewSet

router = DefaultRouter()
router.register(r"client", UserViewSet, basename="customuser")

urlpatterns = [
    path("update_profile_image/<int:pk>", ProfileUpdateView.as_view(), name="profile"),
    path("profile_image/", ProfileSetView.as_view(), name="profile"),
    path('upload-file/', FileUploadAPIView.as_view(), name='upload-file'),
    path('download_file/<int:pk>/', download_file, name='download_file'),
    path("", include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
