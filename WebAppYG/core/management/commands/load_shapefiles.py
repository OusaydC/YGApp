from django.core.management.base import BaseCommand
import geopandas as gpd
import os
import json
from core.models import AdministrativeBoundary

class Command(BaseCommand):
    help = 'Load Morocco shapefiles into the database'
    
    def add_arguments(self, parser):
        parser.add_argument('--shapefile', type=str, help='Path to shapefile')
        parser.add_argument('--level', type=str, default='province', help='Administrative level')
        parser.add_argument('--name-field', type=str, default='NOM_PROV', help='Field name for region names')
        parser.add_argument('--code-field', type=str, default='CODE_PROVI', help='Field name for region codes')
    
    def handle(self, *args, **options):
        shapefile_path = options.get('shapefile')
        level = options.get('level')
        name_field = options.get('name_field')
        code_field = options.get('code_field')
        
        if not shapefile_path:
            # Default to regions shapefile
            shapefile_path = 'data/shapefiles/Concerned_Provinces.shp'
        
        if not os.path.exists(shapefile_path):
            self.stdout.write(
                self.style.ERROR(f'Shapefile not found: {shapefile_path}')
            )
            return
        
        # Read shapefile
        gdf = gpd.read_file(shapefile_path)
        
        # Convert to WGS84 if needed
        if gdf.crs != 'EPSG:4326':
            gdf = gdf.to_crs('EPSG:4326')
        
        self.stdout.write(f'Loaded shapefile with {len(gdf)} features')
        self.stdout.write(f'Available columns: {list(gdf.columns)}')
        
        # Load into database
        for idx, row in gdf.iterrows():
            # Extract name and code from shapefile attributes
            name = row.get(name_field, f'{level}_{idx}')
            code = row.get(code_field, f'{level}_{idx}')
            
            # Convert geometry to GeoJSON
            try:
                geometry_json = row.geometry.__geo_interface__ if hasattr(row.geometry, '__geo_interface__') else None
                if geometry_json:
                    # Simplify geometry for better performance
                    simplified_geom = row.geometry.simplify(tolerance=0.01, preserve_topology=True)
                    geometry_json = simplified_geom.__geo_interface__
            except Exception as e:
                self.stdout.write(f'Error processing geometry for {name}: {e}')
                geometry_json = None
            
            # Create or update boundary
            boundary, created = AdministrativeBoundary.objects.get_or_create(
                code=code,
                defaults={
                    'name': name,
                    'level': level,
                    'geometry_json': json.dumps(geometry_json) if geometry_json else None,
                }
            )
            
            if created:
                self.stdout.write(f'Created: {name} ({code}) - Geometry: {bool(geometry_json)}')
            else:
                # Update geometry if it exists
                if geometry_json:
                    boundary.geometry_json = json.dumps(geometry_json)
                    boundary.save()
                self.stdout.write(f'Updated: {name} ({code}) - Geometry: {bool(geometry_json)}')
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully loaded {len(gdf)} boundaries')
        )