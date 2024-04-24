from django.db import models

class ServiceCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Service(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='services')
    duration = models.DurationField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name