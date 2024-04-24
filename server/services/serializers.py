from rest_framework import serializers
from .models import ServiceCategory, Service

class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=ServiceCategory.objects.all(),
        slug_field='name'
    )

    class Meta:
        model = Service
        fields = '__all__'

    def create(self, validated_data):
        category = validated_data.pop('category')
        service = Service.objects.create(category=category, **validated_data)
        return service

    def update(self, instance, validated_data):
        category_id = validated_data.pop('category', None)
        if category_id:
            category = ServiceCategory.objects.get(id=category_id)
            instance.category = category

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance