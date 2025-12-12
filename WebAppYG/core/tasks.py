from celery import shared_task
from django.contrib.gis.geos import GEOSGeometry
import pandas as pd
from .models import AdministrativeBoundary, Crop, YieldData

@shared_task
def process_yield_data(csv_file_path):
    """Process yield data from CSV file"""
    df = pd.read_csv(csv_file_path)
    
    for _, row in df.iterrows():
        # Process each row
        boundary, created = AdministrativeBoundary.objects.get_or_create(
            code=row['boundary_code'],
            defaults={
                'name': row['boundary_name'],
                'level': row['boundary_level'],
                'geometry': GEOSGeometry(row['geometry'])
            }
        )
        
        crop, created = Crop.objects.get_or_create(
            name=row['crop_name']
        )
        
        yield_data, created = YieldData.objects.get_or_create(
            boundary=boundary,
            crop=crop,
            year=row['year'],
            defaults={
                'actual_yield': row.get('actual_yield'),
                'potential_yield': row.get('potential_yield'),
                'yield_gap': row.get('yield_gap'),
                'yield_gap_percent': row.get('yield_gap_percent'),
                'data_source': row.get('data_source', 'CSV Import')
            }
        )
    
    return f"Processed {len(df)} records"