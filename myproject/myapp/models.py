from django.db import models
from django.contrib.auth.models import User


class Organization(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Section(models.Model):
    name = models.CharField(max_length=255)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='sections')

    def __str__(self):
        return self.name


class Person(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Администратор'),
        ('coach', 'Тренер'),
        ('client', 'Клиент'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='person')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"
