import os
import geopandas as gpd
from django.core.management.base import BaseCommand
from core.models import ParcelPoint
import json


class Command(BaseCommand):
    help = 'Load parcel points from variety shapefiles'

    def add_arguments(self, parser):
        parser.add_argument('--dir', type=str, help='Directory containing variety shapefiles', 
                          default='data/Shapefiles/Varieties')

    def handle(self, *args, **options):
        from django.conf import settings
        from pathlib import Path
        
        shapefile_dir = options['dir']
        
        # Convert to absolute path if relative
        if not os.path.isabs(shapefile_dir):
            base_dir = Path(settings.BASE_DIR)
            shapefile_dir = str(base_dir / shapefile_dir)
        
        if not os.path.exists(shapefile_dir):
            self.stdout.write(self.style.ERROR(f'Directory not found: {shapefile_dir}'))
            # Try to find the directory
            base_dir = Path(settings.BASE_DIR)
            varieties_base = base_dir / 'data' / 'Shapefiles' / 'Varieties'
            if varieties_base.exists():
                self.stdout.write(f'Found Varieties directory at: {varieties_base}')
                # List subdirectories
                for subdir in varieties_base.iterdir():
                    if subdir.is_dir():
                        self.stdout.write(f'  Subdirectory: {subdir.name}')
                        for shp in subdir.glob('*.shp'):
                            self.stdout.write(f'    - {shp.name}')
            return

        # Clear existing parcel points
        ParcelPoint.objects.all().delete()
        self.stdout.write('Cleared existing parcel points')

        # List of variety shapefiles
        variety_files = [
            'Achtar.shp',
            'Arrehane.shp', 
            'Bandera.shp',
            'Faiza.shp',
            'Radia.shp'
        ]

        created_count = 0
        
        # Convert to Path object
        if isinstance(shapefile_dir, str):
            if os.path.isabs(shapefile_dir):
                base_varieties_dir = Path(shapefile_dir)
            else:
                base_varieties_dir = Path(settings.BASE_DIR) / shapefile_dir
        else:
            base_varieties_dir = shapefile_dir
        
        for variety_file in variety_files:
            # Try direct path first
            file_path = base_varieties_dir / variety_file
            
            # If not found, search in subdirectories
            if not file_path.exists() and base_varieties_dir.exists():
                for subdir in base_varieties_dir.iterdir():
                    if subdir.is_dir():
                        potential_path = subdir / variety_file
                        if potential_path.exists():
                            file_path = potential_path
                            self.stdout.write(f'Found {variety_file} in subdirectory: {subdir.name}')
                            break
            
            file_path = str(file_path)
            
            if not os.path.exists(file_path):
                self.stdout.write(self.style.WARNING(f'Shapefile not found: {file_path}'))
                continue
                
            try:
                self.stdout.write(f'Loading {variety_file}...')
                
                # Read shapefile
                gdf = gpd.read_file(file_path)
                
                # Convert to WGS84 if needed
                if gdf.crs and gdf.crs != 'EPSG:4326':
                    gdf = gdf.to_crs('EPSG:4326')
                
                # Simplify geometries for better performance
                gdf['geometry'] = gdf['geometry'].simplify(tolerance=0.001)
                
                self.stdout.write(f'Loaded {len(gdf)} features from {variety_file}')
                self.stdout.write(f'Columns: {list(gdf.columns)}')
                
                # Extract variety name from filename
                variety_name = variety_file.replace('.shp', '')
                
                # Process each feature
                for index, row in gdf.iterrows():
                    try:
                        # Get geometry centroid
                        centroid = row.geometry.centroid
                        lon = centroid.x
                        lat = centroid.y
                        
                        # Check if coordinates are in Morocco range
                        if not (-17 <= lon <= -1 and 21 <= lat <= 36):
                            self.stdout.write(self.style.WARNING(f'Skipping point outside Morocco: {lon}, {lat}'))
                            continue
                        
                        # Create parcel points for each year
                        for year in [2019, 2020, 2021]:
                            parcel = ParcelPoint.objects.create(
                                x=lon,
                                y=lat,
                                parcel_id=f'{variety_name}_{index}_{year}',
                                province='Unknown',  # Will be updated if we have province data
                                variety=variety_name,
                                year=year,
                                area=1.0,   # Default area
                                yield_total=0.0,  # Default yield
                                yield_per_ha=0.0  # Default yield per ha
                            )
                        
                        created_count += 3  # 3 years per point
                        
                    except Exception as e:
                        self.stdout.write(self.style.WARNING(f'Error creating parcel {index} from {variety_file}: {e}'))
                        continue
                        
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error loading {variety_file}: {e}'))
                continue

        self.stdout.write(self.style.SUCCESS(f'Successfully loaded {created_count} parcel points from variety shapefiles'))
