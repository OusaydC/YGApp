from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from core.models import (
    AdministrativeBoundary, Crop, YieldData,
    Variety, Scenario, YieldStatistics, GapType, GapStatistics
)
from .serializers import (
    AdministrativeBoundarySerializer, CropSerializer, YieldDataSerializer,
    VarietySerializer, ScenarioSerializer, YieldStatisticsSerializer,
    GapTypeSerializer, GapStatisticsSerializer
)

class AdministrativeBoundaryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AdministrativeBoundary.objects.all()
    serializer_class = AdministrativeBoundarySerializer

class CropViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Crop.objects.all()
    serializer_class = CropSerializer

class YieldDataViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = YieldData.objects.all()
    serializer_class = YieldDataSerializer
    
    @action(detail=False, methods=['get'])
    def by_region(self, request):
        region_id = request.query_params.get('region_id')
        crop_id = request.query_params.get('crop_id')
        year = request.query_params.get('year')
        
        queryset = self.get_queryset()
        if region_id:
            queryset = queryset.filter(boundary_id=region_id)
        if crop_id:
            queryset = queryset.filter(crop_id=crop_id)
        if year:
            queryset = queryset.filter(year=year)
            
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class VarietyViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for wheat varieties"""
    queryset = Variety.objects.all()
    serializer_class = VarietySerializer


class ScenarioViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for yield scenarios"""
    queryset = Scenario.objects.all()
    serializer_class = ScenarioSerializer


class YieldStatisticsViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for yield statistics with filtering"""
    queryset = YieldStatistics.objects.all().select_related('variety', 'scenario')
    serializer_class = YieldStatisticsSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['variety', 'province', 'year', 'scenario']
    ordering_fields = ['year', 'mean', 'province']
    ordering = ['-year']
    
    @action(detail=False, methods=['get'])
    def filter_data(self, request):
        """
        Custom endpoint for advanced filtering
        Query params: variety, province, year, scenario
        """
        queryset = self.get_queryset()
        
        variety_id = request.query_params.get('variety')
        province = request.query_params.get('province')
        year = request.query_params.get('year')
        scenario_id = request.query_params.get('scenario')
        
        if variety_id:
            queryset = queryset.filter(variety_id=variety_id)
        if province:
            queryset = queryset.filter(province=province)
        if year:
            queryset = queryset.filter(year=year)
        if scenario_id:
            queryset = queryset.filter(scenario_id=scenario_id)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def provinces(self, request):
        """Get list of unique provinces"""
        provinces = YieldStatistics.objects.exclude(
            province__isnull=True
        ).values_list('province', flat=True).distinct().order_by('province')
        return Response(list(provinces))
    
    @action(detail=False, methods=['get'])
    def years(self, request):
        """Get list of unique years"""
        years = YieldStatistics.objects.exclude(
            year__isnull=True
        ).values_list('year', flat=True).distinct().order_by('year')
        return Response(list(years))
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get summary statistics"""
        variety_id = request.query_params.get('variety')
        province = request.query_params.get('province')
        year = request.query_params.get('year')
        
        queryset = self.get_queryset()
        
        if variety_id:
            queryset = queryset.filter(variety_id=variety_id)
        if province:
            queryset = queryset.filter(province=province)
        if year:
            queryset = queryset.filter(year=year)
        
        # Group by scenario and calculate averages
        summary = {}
        for stat in queryset:
            scenario_name = stat.scenario.name if stat.scenario else 'Overall'
            if scenario_name not in summary:
                summary[scenario_name] = {
                    'mean': stat.mean,
                    'min': stat.min,
                    'max': stat.max,
                    'median': stat.median,
                    'count': stat.count
                }
        
        return Response(summary)


class GapTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for gap types"""
    queryset = GapType.objects.all()
    serializer_class = GapTypeSerializer


class GapStatisticsViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for gap statistics with filtering"""
    queryset = GapStatistics.objects.all().select_related('gap_type', 'variety')
    serializer_class = GapStatisticsSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['gap_type', 'variety', 'province', 'year']
    ordering_fields = ['year', 'mean', 'province']
    ordering = ['-year']
    
    @action(detail=False, methods=['get'])
    def filter_data(self, request):
        """
        Custom endpoint for advanced filtering
        Query params: gap_type, variety, province, year
        """
        queryset = self.get_queryset()
        
        gap_type_id = request.query_params.get('gap_type')
        variety_id = request.query_params.get('variety')
        province = request.query_params.get('province')
        year = request.query_params.get('year')
        
        if gap_type_id:
            queryset = queryset.filter(gap_type_id=gap_type_id)
        if variety_id:
            queryset = queryset.filter(variety_id=variety_id)
        if province:
            queryset = queryset.filter(province=province)
        if year:
            queryset = queryset.filter(year=year)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def provinces(self, request):
        """Get list of unique provinces"""
        provinces = GapStatistics.objects.exclude(
            province__isnull=True
        ).values_list('province', flat=True).distinct().order_by('province')
        return Response(list(provinces))
    
    @action(detail=False, methods=['get'])
    def years(self, request):
        """Get list of unique years"""
        years = GapStatistics.objects.exclude(
            year__isnull=True
        ).values_list('year', flat=True).distinct().order_by('year')
        return Response(list(years))
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get summary statistics"""
        variety_id = request.query_params.get('variety')
        province = request.query_params.get('province')
        year = request.query_params.get('year')
        
        queryset = self.get_queryset()
        
        if variety_id:
            queryset = queryset.filter(variety_id=variety_id)
        if province:
            queryset = queryset.filter(province=province)
        if year:
            queryset = queryset.filter(year=year)
        
        # Group by gap type and calculate averages
        summary = {}
        for stat in queryset:
            gap_type_name = stat.gap_type.name if stat.gap_type else 'Overall'
            if gap_type_name not in summary:
                summary[gap_type_name] = {
                    'mean': stat.mean,
                    'min': stat.min,
                    'max': stat.max,
                    'median': stat.median,
                    'count': stat.count
                }
        
        return Response(summary)


def yield_data_api(request):
    data = list(YieldData.objects.values(
        'boundary__name', 'crop__name', 'year', 
        'actual_yield', 'potential_yield', 'yield_gap'
    ))
    return JsonResponse(data, safe=False)