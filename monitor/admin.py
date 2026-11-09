from django.contrib import admin
from .models import Reading,Alert
@admin.register(Reading)
class ReadingAdmin(admin.ModelAdmin):
 list_display=('received_at','station_id','water_level_cm','risk','simulated')
 list_filter=('risk','simulated','station_id')
@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
 list_display=('created_at','severity','message')
