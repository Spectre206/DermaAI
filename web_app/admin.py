from django.contrib import admin
from .models import SkinLesionScan

@admin.register(SkinLesionScan)
class SkinScanAdmin(admin.ModelAdmin):
    list_display = ('patient', 'prediction', 'confidence', 'created_at')
    list_filter = ('prediction', 'created_at')
    search_fields = ('patient__username', 'prediction')
    readonly_fields = ('created_at',)