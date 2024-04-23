from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
import uuid


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, user_type=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, user_type=user_type, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser):
    class Types(models.TextChoices):
        business_owner = "Business Owner"
        beauty_professional = "Beauty Professional"
        retail_customer = "Retail Customer"
    
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    user_type = models.CharField(
        max_length=20,
        choices=Types.choices,
    )
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['location', 'user_type']
    
    objects = CustomUserManager()
    

class BusinessOwnerManager(CustomUserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(user_type=User.Types.business_owner)
    
class BeautyProfessionalManager(CustomUserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(user_type=User.Types.beauty_professional)

class RetailManager(CustomUserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(user_type=User.Types.retail_customer)
    
class BusinessOwnerMore(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=255)
    rating = models.FloatField(default=0.0)


class BusinessOwner(User):
    objects = BusinessOwnerManager()

    @property
    def more(self):
        return self.businessownermore
    
    @property
    def user_profile(self):
        return self.profile

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.user_type = User.Types.business_owner
        return super().save(*args, **kwargs)
    

class BeautyProfessionalMore(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.FloatField(default=0.0)
    experience_level = models.IntegerField(default=0)
    availability = models.TextField(blank=True)


class BeautyProfessional(User):
    objects = BeautyProfessionalManager()

    @property
    def more(self):
        return self.beautyprofessionalmore
    
    @property
    def user_profile(self):
        return self.profile

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.user_type = User.Types.beauty_professional
        return super().save(*args, **kwargs)
    

class RetailCustomer(User):
    objects = RetailManager()

    @property
    def user_profile(self):
        return self.profile 

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.user_type = User.Types.retail_customer
        return super().save(*args, **kwargs)
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f"{self.user.email}'s profile"