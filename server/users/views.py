from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .serializers import (
    BusinessOwnerSerializer,
    BeautyProfessionalSerializer,
    RetailCustomerSerializer
)
from .models import (
    BusinessOwner,
    BeautyProfessional,
    RetailCustomer
)

class BusinessOwnerViewSet(viewsets.ModelViewSet):
    queryset = BusinessOwner.objects.all()
    serializer_class = BusinessOwnerSerializer
    permission_classes = [AllowAny]

class BeautyProfessionalViewSet(viewsets.ModelViewSet):
    queryset = BeautyProfessional.objects.all()
    serializer_class = BeautyProfessionalSerializer
    permission_classes = [AllowAny]

class RetailCustomerViewSet(viewsets.ModelViewSet):
    queryset = RetailCustomer.objects.all()
    serializer_class = RetailCustomerSerializer
    permission_classes = [AllowAny]