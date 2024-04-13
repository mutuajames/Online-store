from django.db import IntegrityError, transaction
from .models import BeautyProfessionalMore, BusinessOwner, BeautyProfessional, BusinessOwnerMore, RetailCustomer
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
# from djoser.serializers import UserCreateSerializer as DjoserUserCreateSerializer
from rest_framework import serializers
# from .models import RetailCustomer, BusinessOwner, BeautyProfessional
from rest_framework.serializers import raise_errors_on_nested_writes, ModelSerializer
from rest_framework.utils import model_meta
from rest_framework.exceptions import ParseError
from typing import Dict


User = get_user_model()

def create_user_by_validated_data(user: User, user_more=None, **validated_data: Dict) -> User: # type: ignore
    if not user_more:
        return user.objects.create_user(**validated_data)

    extra_fields, validated_data = retrieve_extra_fields(**validated_data)
    print(user)
    user = user.objects.create_user(**validated_data)
    user_more.objects.create(user=user, **extra_fields)
    print(user)
    print("Extra fields:", extra_fields)
    return user


def retrieve_extra_fields(**validated_data):
    extra_fields = validated_data.pop('more')
    return extra_fields, validated_data

class CustomModelSerializer(ModelSerializer):
    def update(self, instance, validated_data):
        print(instance, validated_data)
        raise_errors_on_nested_writes('update', self, validated_data)
        info = model_meta.get_field_info(instance)

        extra_fields, validated_data = retrieve_extra_fields(**validated_data)

        m2m_fields = []
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                m2m_fields.append((attr, value))
            else:
                setattr(instance, attr, value)

        for attr, value in extra_fields.items():
            setattr(instance.more, attr, value)

        instance.save()
        instance.more.save()

        for attr, value in m2m_fields:
            field = getattr(instance, attr)
            field.set(value)

        return instance

class BusinessOwnerMoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessOwnerMore
        fields = ('business_name', 'rating')

class BusinessOwnerSerializer(serializers.ModelSerializer):
    more = BusinessOwnerMoreSerializer()

    class Meta:
        model = BusinessOwner
        fields = ('id', 'first_name', 'last_name', 'email', 'location', 'user_type', 'phone_number', 'more')

    def create(self, validated_data):
        return create_user_by_validated_data(BusinessOwner, BusinessOwnerMore, **validated_data)


class BeautyProfessionalMoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = BeautyProfessionalMore
        fields = ('rating', 'experience_level', 'availability')

class BeautyProfessionalSerializer(CustomModelSerializer):
    more = BeautyProfessionalMoreSerializer()

    class Meta:
        model = BeautyProfessional
        fields = ('id', 'first_name', 'last_name', 'email', 'location', 'user_type', 'phone_number', 'more')

    def create(self, validated_data):
        print("BeautyProfessionalSerializer create input:", validated_data)

        return create_user_by_validated_data(BeautyProfessional, BeautyProfessionalMore, **validated_data)

class RetailCustomerSerializer(CustomModelSerializer):
    class Meta:
        model = RetailCustomer
        fields = ('id', 'first_name', 'last_name', 'email', 'location', 'user_type', 'phone_number')

    def create(self, validated_data):
        return create_user_by_validated_data(RetailCustomer, **validated_data)



class CustomUserSerializer(serializers.ModelSerializer):
    """User serializer to create, retrieve a user and get list of users"""

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'user_type', 'location', 'phone_number')


class CustomUserCreateSerializer(UserCreateSerializer):
    """Rewriting the creation of user for djoser"""

    def create(self, validated_data):
        print(validated_data)
        try:
            user = self.perform_create(validated_data)
        except IntegrityError:
            # Todo: log this exception as critical while creating user
            self.fail("cannot_create_user")

        return user

    def perform_create(self, validated_data):
        with transaction.atomic():
            user = create_user_by_type(**validated_data)
            # if settings.SEND_ACTIVATION_EMAIL:
            #     user.is_active = False
            #     user.save(update_fields=["is_active"])
        return user
    

_USER_TYPES = {  # only these users can create products
    'Business Owner': (BusinessOwner, BusinessOwnerMore),
    'Beauty Professional': (BeautyProfessional, BeautyProfessionalMore),
    'Retail Customer': (RetailCustomer),
}


def _create_user(user_model, user_more, **validated_data):
    try:
        user = user_model.objects.create_user(**validated_data)
        print(user)
        user_more.objects.create(user=user)
        return user
    except Exception:
        # Todo: log the exception as error
        raise ParseError("Error while creating user.")
    

def create_user_by_type(**validated_data: Dict):
    """Creating corresponding user object by user type"""
    user_type = validated_data.pop('user_type')

    print(validated_data)

    for user_type_key, user_objects in _USER_TYPES.items():
        UserModel, UserMoreModel = user_objects

        if user_type.lower() == user_type_key:
            return _create_user(
                user_model=UserModel,
                user_more=UserMoreModel,
                **validated_data
            )

