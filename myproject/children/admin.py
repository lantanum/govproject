from django.contrib import admin
from .models import Child

@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'iin', 'birth_date', 'qr_code_display')
    list_filter = ('birth_date',)
    search_fields = ('full_name', 'iin')
    readonly_fields = ('qr_code',)

    def qr_code_display(self, obj):
        if obj.qr_code:
            return f"<img src='{obj.qr_code.url}' alt='QR Code' style='width:100px; height:100px;' />"
        return "QR Code not generated"
    qr_code_display.short_description = "QR Code"
    qr_code_display.allow_tags = True
