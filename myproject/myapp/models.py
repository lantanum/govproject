# models.py

from django.db import models
from django.contrib.auth.models import User

class Organization(models.Model):
    name = models.CharField(max_length=255, unique=True)
    director = models.OneToOneField(
        "Person",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="organization_director",
    )

    def __str__(self):
        return self.name



class Section(models.Model):
    name = models.CharField(max_length=255)
    start_time = models.TimeField(default="00:00")
    end_time = models.TimeField(default="23:59")  # default time, change as needed
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name='sections')
    

    def __str__(self):
        return f"{self.name} ({self.start_time} - {self.end_time})"

    def save(self, *args, **kwargs):
        # Ensure start time is not greater than end time
        if self.start_time >= self.end_time:
            raise ValueError("End time cannot be earlier than start time.")
        super().save(*args, **kwargs)


class Person(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Администратор'),
        ('coach', 'Тренер'),
        ('client', 'Клиент'),
        ('director', 'Руководитель'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='person')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=True)
    sections = models.ManyToManyField(Section, related_name="participants", blank=True)  # Новая связь

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"



class Attendance(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='attendances')
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='attendances')
    visit_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Посещение {self.person.user.username} на секции {self.section.name} - {self.visit_date}"
