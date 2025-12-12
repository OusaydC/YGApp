from django.contrib import admin
from .models import (
    AdministrativeBoundary, Crop, YieldData, ParcelPoint,
    Variety, Scenario, YieldStatistics, GapType, GapStatistics
)

@admin.register(AdministrativeBoundary)
class AdministrativeBoundaryAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'level', 'created_at']
    list_filter = ['level', 'created_at']
    search_fields = ['name', 'code']
    readonly_fields = ['created_at']

@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ['name', 'scientific_name']
    search_fields = ['name', 'scientific_name']

@admin.register(YieldData)
class YieldDataAdmin(admin.ModelAdmin):
    list_display = ['boundary', 'crop', 'year', 'actual_yield', 'potential_yield', 'yield_gap', 'data_source']
    list_filter = ['crop', 'year', 'data_source']
    search_fields = ['boundary__name', 'crop__name']
    readonly_fields = ['created_at']
    fieldsets = (
        ('Basic Info', {
            'fields': ('boundary', 'crop', 'year', 'data_source')
        }),
        ('Yield Levels (t/ha)', {
            'fields': ('potential_yield', 'water_limited_yield', 'nutrient_limited_yield', 
                      'actual_yield', 'unfertilized_yield')
        }),
        ('Yield Gap Decomposition (t/ha)', {
            'fields': ('yield_gap', 'yield_gap_percent', 'water_gap', 'nutrient_gap', 
                      'management_gap', 'fertilizer_response_gap')
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('boundary', 'crop')

@admin.register(ParcelPoint)
class ParcelPointAdmin(admin.ModelAdmin):
    list_display = ['parcel_id', 'province', 'variety', 'year', 'yield_per_ha', 'area']
    list_filter = ['province', 'variety', 'year']
    search_fields = ['parcel_id', 'province', 'variety']
    readonly_fields = ['created_at']


@admin.register(Variety)
class VarietyAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']


@admin.register(Scenario)
class ScenarioAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']


@admin.register(YieldStatistics)
class YieldStatisticsAdmin(admin.ModelAdmin):
    list_display = ['variety', 'province', 'year', 'scenario', 'mean', 'median', 'count', 'data_source']
    list_filter = ['variety', 'scenario', 'year', 'province']
    search_fields = ['province', 'variety__name', 'scenario__name']
    readonly_fields = ['created_at', 'updated_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('variety', 'scenario')


@admin.register(GapType)
class GapTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']


@admin.register(GapStatistics)
class GapStatisticsAdmin(admin.ModelAdmin):
    list_display = ['gap_type', 'variety', 'province', 'year', 'mean', 'median', 'count', 'data_source']
    list_filter = ['gap_type', 'variety', 'year', 'province']
    search_fields = ['province', 'variety__name', 'gap_type__name']
    readonly_fields = ['created_at', 'updated_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('gap_type', 'variety')