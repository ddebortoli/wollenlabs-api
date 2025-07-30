from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import UrlCheckViewSet

router = DefaultRouter()
router.register(r'url-checks', UrlCheckViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]