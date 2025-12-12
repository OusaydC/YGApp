from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from .models import AdministrativeBoundary, Crop, YieldData, ParcelPoint

def map_view(request):
    return render(request, 'map.html')

def api_yield_data(request):
    # Get filter parameters
    crop_name = request.GET.get('crop', '')
    year = request.GET.get('year', '')
    metric = request.GET.get('metric', 'actual_yield')
    
    # Build query
    queryset = YieldData.objects.select_related('boundary', 'crop')
    
    if crop_name:
        queryset = queryset.filter(crop__name=crop_name)
    if year:
        queryset = queryset.filter(year=int(year))
    
    # Get data with geometry
    data = []
    for yield_data in queryset:
        item = {
            'id': yield_data.id,
            'boundary_name': yield_data.boundary.name,
            'boundary_code': yield_data.boundary.code,
            'crop_name': yield_data.crop.name,
            'year': yield_data.year,
            # Yield levels
            'actual_yield': yield_data.actual_yield,
            'potential_yield': yield_data.potential_yield,
            'water_limited_yield': yield_data.water_limited_yield,
            'nutrient_limited_yield': yield_data.nutrient_limited_yield,
            'unfertilized_yield': yield_data.unfertilized_yield,
            # Basic gaps
            'yield_gap': yield_data.yield_gap,
            'yield_gap_percent': yield_data.yield_gap_percent,
            # Decomposed gaps
            'water_gap': yield_data.water_gap,
            'nutrient_gap': yield_data.nutrient_gap,
            'management_gap': yield_data.management_gap,
            'fertilizer_response_gap': yield_data.fertilizer_response_gap,
            # Geometry
            'geometry': yield_data.boundary.geometry_json,
            'metric_value': getattr(yield_data, metric, None)
        }
        data.append(item)
    
    return JsonResponse(data, safe=False)

def api_boundaries(request):
    data = list(AdministrativeBoundary.objects.values(
        'id', 'name', 'code', 'level', 'geometry_json'
    ))
    return JsonResponse(data, safe=False)

def api_crops(request):
    data = list(Crop.objects.values('id', 'name', 'scientific_name'))
    return JsonResponse(data, safe=False)

def api_years(request):
    # Return real years + Average (9999)
    years = list(YieldData.objects.values_list('year', flat=True).distinct().order_by('year'))
    
    # Add real years and Average
    if not years:
        years = [2019, 2020, 2021, 9999]  # 9999 = Average
    elif 9999 not in years:
        years.append(9999)
    
    return JsonResponse(sorted(years), safe=False)

def export_csv(request):
    import csv
    from django.http import HttpResponse
    
    # Get filter parameters
    crop_name = request.GET.get('crop', '')
    year = request.GET.get('year', '')
    
    # Build query
    queryset = YieldData.objects.select_related('boundary', 'crop')
    
    if crop_name:
        queryset = queryset.filter(crop__name=crop_name)
    if year:
        queryset = queryset.filter(year=int(year))
    
    # Create CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="yield_data.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Region', 'Crop', 'Year', 'Actual Yield (t/ha)', 'Potential Yield (t/ha)', 'Yield Gap (t/ha)', 'Yield Gap (%)', 'Data Source'])
    
    for yield_data in queryset:
        writer.writerow([
            yield_data.boundary.name,
            yield_data.crop.name,
            yield_data.year,
            yield_data.actual_yield,
            yield_data.potential_yield,
            yield_data.yield_gap,
            yield_data.yield_gap_percent,
            yield_data.data_source
        ])
    
    return response

def api_parcel_points(request):
    # Get filter parameters
    province = request.GET.get('province', '')
    variety = request.GET.get('variety', '')
    year = request.GET.get('year', '')
    
    # Build query
    queryset = ParcelPoint.objects.all()
    
    if province:
        queryset = queryset.filter(province__icontains=province)
    if variety:
        queryset = queryset.filter(variety__icontains=variety)
    if year:
        queryset = queryset.filter(year=int(year))
    
    # Get data
    data = []
    for parcel in queryset:
        item = {
            'id': parcel.id,
            'x': parcel.x,
            'y': parcel.y,
            'parcel_id': parcel.parcel_id,
            'province': parcel.province,
            'variety': parcel.variety,
            'year': parcel.year,
            'area': parcel.area,
            'yield_total': parcel.yield_total,
            'yield_per_ha': parcel.yield_per_ha
        }
        data.append(item)
    
    return JsonResponse(data, safe=False)