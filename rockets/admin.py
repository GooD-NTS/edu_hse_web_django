from django.contrib import admin
from .models import Rocket, Cosmodrome, Launch


@admin.register(Rocket)
class RocketAdmin(admin.ModelAdmin):
    list_display = ['name', 'manufacturer', 'country', 'rocket_type', 'status', 'first_flight_year']
    list_filter = ['rocket_type', 'status', 'country']
    search_fields = ['name', 'manufacturer', 'country', 'description']
    ordering = ['name']


@admin.register(Cosmodrome)
class CosmodromeAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'location', 'founded_year', 'is_active']
    list_filter = ['country', 'is_active']
    search_fields = ['name', 'country', 'location', 'description']
    ordering = ['name']


@admin.register(Launch)
class LaunchAdmin(admin.ModelAdmin):
    list_display = ['mission_name', 'rocket', 'cosmodrome', 'launch_date', 'status']
    list_filter = ['status', 'rocket', 'cosmodrome', 'launch_date']
    search_fields = ['mission_name', 'payload', 'description', 'rocket__name', 'cosmodrome__name']
    ordering = ['-launch_date']
    date_hierarchy = 'launch_date'
