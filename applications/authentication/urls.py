from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView

from . import views as v

from .routers import router

urlpatterns = [
    # Authentication url to take token
    path("token/", v.CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    path("update_profile_image/<int:pk>", v.ProfileUpdateView.as_view(), name="profile"),
    path("profile_image/", v.ProfileSetView.as_view(), name="profile"),
    path('upload-file/', v.FileUploadAPIView.as_view(), name='upload-file'),
    path('download_file/<int:pk>/', v.download_file, name='download_file'),
    path("", include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
