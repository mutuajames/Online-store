from django.urls import include, path, re_path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from .views import (
    # UserViewSet,
    BusinessOwnerViewSet,
    BeautyProfessionalViewSet,
    RetailCustomerViewSet
)

router = DefaultRouter()
# router.register('users', UserViewSet, basename='users')
router.register('business-owners', BusinessOwnerViewSet, basename='business-owners')
router.register('beauty-professionals', BeautyProfessionalViewSet, basename='beauty-professionals')
router.register('retail-customers', RetailCustomerViewSet, basename='retail-customers')

urlpatterns = [
    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.jwt')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]
