from django.db import models

class Child(models.Model):
    iin = models.CharField(max_length=12, unique=True)
    full_name = models.CharField(max_length=255)
    birth_date = models.DateField()
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    def __str__(self):
        return self.full_name
