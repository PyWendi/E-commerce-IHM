from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView

from .views_class.CustomuserViewClass import CustomTokenObtainPairView
from .views_class.SubFunction import set_password, download_file
from .views_class.ProfileSetViewClass import ProfileSetView
from .views_class.FileUploadViewClass import FileUploadAPIView

# from . import views as v

from .routers import router

urlpatterns = [
    # Authentication url to take token
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("set_password/<str:password>", set_password, name="password_setter"),

    path("profile_image/", ProfileSetView.as_view(), name="profile"),
    path('upload-file/', FileUploadAPIView.as_view(), name='upload-file'),
    path('download_file/<int:pk>/', download_file, name='download_file'),
    path("", include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
