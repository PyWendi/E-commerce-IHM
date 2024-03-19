from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from django.contrib import admin
from django.urls import path, include

"""
Setting for the entire API discovery using swagger through openAPI
"""
schema_view = get_schema_view(
    openapi.Info(
        title="E-Commerce API's",
        default_version="v1",
        description="La liste de tous les point d'entrer des API ainsi que les variables de body",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)



urlpatterns = [
    # Authentication URL/API
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework"), name="api.login.logout"),
    # path("api-token-auth/", views.obtain_auth_token),
    # Admin URL
    path('admin/', admin.site.urls),

    # SWAGGER URL
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path("api/", include("applications.authentication.urls")),
    path("api/", include("applications.product.urls")),
]
