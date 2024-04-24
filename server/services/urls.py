from django.urls import path, include
from rest_framework import routers

from .views import ServiceCategoryViewSet, ServiceViewSet

router = routers.DefaultRouter()
router.register(r'service-categories', ServiceCategoryViewSet)
router.register(r'services', ServiceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]