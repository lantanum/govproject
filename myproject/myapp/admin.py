from django.contrib import admin
from .models import Organization, Section, Person, Attendance

admin.site.register(Person)
admin.site.register(Attendance)
admin.site.register(Organization)
admin.site.register(Section)