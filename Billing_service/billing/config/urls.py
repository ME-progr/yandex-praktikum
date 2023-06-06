from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
schema_view = get_schema_view(
   openapi.Info(
      title="Billing service API",
      default_version='v1',
      description="API для лучшего биллинга в лучшем кинтотеатре",
      contact=openapi.Contact(email="bexram33@mail.ru"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
   path("admin/", admin.site.urls),
   path("billing/api/", include("billing.api.urls")),
]

urlpatterns += [
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
