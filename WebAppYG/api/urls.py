from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import api_crops, api_years, api_boundaries, api_yield_data, export_csv, api_parcel_points
from .views import (
    VarietyViewSet, ScenarioViewSet, YieldStatisticsViewSet,
    GapTypeViewSet, GapStatisticsViewSet
)

# Create router for new viewsets
router = DefaultRouter()
router.register(r'varieties', VarietyViewSet, basename='variety')
router.register(r'scenarios', ScenarioViewSet, basename='scenario')
router.register(r'yield-statistics', YieldStatisticsViewSet, basename='yield-statistics')
router.register(r'gap-types', GapTypeViewSet, basename='gap-type')
router.register(r'gap-statistics', GapStatisticsViewSet, basename='gap-statistics')

urlpatterns = [
    # Legacy function-based views
    path('crops/', api_crops, name='api_crops'),
    path('years/', api_years, name='api_years'),
    path('boundaries/', api_boundaries, name='api_boundaries'),
    path('yield-data/', api_yield_data, name='api_yield_data'),
    path('parcel-points/', api_parcel_points, name='api_parcel_points'),
    path('export-csv/', export_csv, name='export_csv'),
    
    # New REST API endpoints
    path('', include(router.urls)),
]