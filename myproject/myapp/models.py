from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class Person(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Администратор'),
        ('coach', 'Тренер'),
        ('client', 'Клиент'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='client')

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # Уникальное имя для обратной связи
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions',  # Уникальное имя для обратной связи
        blank=True
    )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
class Organization(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Section(models.Model):
    name = models.CharField(max_length=255)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='sections')

    def __str__(self):
        return f"{self.name} ({self.organization.name})"

class Attendance(models.Model):
    client = models.ForeignKey(Person, on_delete=models.CASCADE, limit_choices_to={'role': 'client'})
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client.username} - {self.section.name} - {self.timestamp}"
