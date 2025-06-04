from django.contrib import admin
from .models import GliderMeasurement

@admin.register(GliderMeasurement)
class GliderMeasurementAdmin(admin.ModelAdmin):
    list_display = (
        'timestamp', 'latitude', 'longitude', 'depth',
        'temperature', 'salinity', 'oxygen', 'cdom'
    )
    search_fields = ('timestamp',)
    list_filter = ('depth', 'temperature', 'salinity', 'oxygen', 'cdom')