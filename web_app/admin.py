from django.contrib import admin
from .models import SkinLesionScan,Feedback

@admin.register(SkinLesionScan)
class SkinScanAdmin(admin.ModelAdmin):
    list_display = ('patient', 'prediction', 'confidence', 'created_at')
    list_filter = ('prediction', 'created_at')
    search_fields = ('patient__username', 'prediction')
    readonly_fields = ('created_at',)

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject', 'rating', 'created_at')  
    list_filter = ('rating', 'created_at')                      
    search_fields = ('user__username', 'subject', 'message')    
    readonly_fields = ('created_at',)