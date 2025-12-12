from rest_framework import serializers
from core.models import (
    AdministrativeBoundary, Crop, YieldData, 
    Variety, Scenario, YieldStatistics, GapType, GapStatistics
)

class AdministrativeBoundarySerializer(serializers.ModelSerializer):
    class Meta:
        model = AdministrativeBoundary
        fields = '__all__'

class CropSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crop
        fields = '__all__'

class YieldDataSerializer(serializers.ModelSerializer):
    boundary_name = serializers.CharField(source='boundary.name', read_only=True)
    crop_name = serializers.CharField(source='crop.name', read_only=True)
    
    class Meta:
        model = YieldData
        fields = '__all__'


class VarietySerializer(serializers.ModelSerializer):
    class Meta:
        model = Variety
        fields = '__all__'


class ScenarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scenario
        fields = '__all__'


class YieldStatisticsSerializer(serializers.ModelSerializer):
    variety_name = serializers.CharField(source='variety.name', read_only=True)
    scenario_name = serializers.CharField(source='scenario.name', read_only=True)
    
    class Meta:
        model = YieldStatistics
        fields = [
            'id', 'variety', 'variety_name', 'province', 'year', 
            'scenario', 'scenario_name', 'count', 'mean', 'std', 
            'min', 'q25', 'median', 'q75', 'max', 
            'data_source', 'created_at', 'updated_at'
        ]


class GapTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GapType
        fields = '__all__'


class GapStatisticsSerializer(serializers.ModelSerializer):
    gap_type_name = serializers.CharField(source='gap_type.name', read_only=True)
    variety_name = serializers.CharField(source='variety.name', read_only=True)
    
    class Meta:
        model = GapStatistics
        fields = [
            'id', 'gap_type', 'gap_type_name', 'variety', 'variety_name', 
            'province', 'year', 'count', 'mean', 'std', 
            'min', 'q25', 'median', 'q75', 'max', 
            'data_source', 'created_at', 'updated_at'
        ]