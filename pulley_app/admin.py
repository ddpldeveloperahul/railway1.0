from django.contrib import admin
from pulley_app.models import PulleyDetection,DetectionRecord



@admin.register(PulleyDetection)
class PulleyDetectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'pole_name', 'uploaded_image', 'result_image', 'distances', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('user__email', 'distances', 'pole_name')


@admin.register(DetectionRecord)
class DetectionRecordAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'user', 'pole_name', 'pulley_count', 'total', 'loss_mm', 'temperature_c', 'htl_value', 'image_path')
    list_filter = ('timestamp', 'pulley_count', 'temperature_c', 'htl_value')
    search_fields = ('timestamp', 'image_path', 'user__email', 'user__username', 'pole_name')
    readonly_fields = ('timestamp', 'image_path')
    ordering = ('-timestamp',)
    
    fieldsets = (
        ('Timestamp', {
            'fields': ('timestamp', 'user', 'pole_name')
        }),
        ('Distance Measurements (mm)', {
            'fields': ('dist12', 'dist23', 'total')
        }),
        ('Expected Values (mm)', {
            'fields': ('expected_total', 'expected_dist12', 'expected_dist23')
        }),
        ('Analysis', {
            'fields': ('loss_mm', 'pulley_count', 'temperature_c', 'htl_value', 'points_json')
        }),
    )
