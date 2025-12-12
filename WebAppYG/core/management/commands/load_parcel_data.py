import pandas as pd
from django.core.management.base import BaseCommand
from core.models import ParcelPoint
import os
from pyproj import Transformer

class Command(BaseCommand):
    help = 'Load parcel data from Excel file'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str, help='Path to Excel file', 
                          default='data/plot_v_p.xlsx')

    def handle(self, *args, **options):
        file_path = options['file']
        
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'File not found: {file_path}'))
            return

        try:
            # Read Excel file
            df = pd.read_excel(file_path)
            
            # Debug: Print column names
            self.stdout.write(f'Excel columns found: {list(df.columns)}')
            self.stdout.write(f'First few rows:')
            self.stdout.write(str(df.head()))
            
            # Check coordinate ranges to detect CRS
            x_vals = df['X'].dropna() if 'X' in df.columns else pd.Series()
            y_vals = df['Y'].dropna() if 'Y' in df.columns else pd.Series()
            
            if len(x_vals) > 0:
                x_min, x_max = x_vals.min(), x_vals.max()
                y_min, y_max = y_vals.min(), y_vals.max()
                self.stdout.write(f'X range: {x_min} to {x_max}')
                self.stdout.write(f'Y range: {y_min} to {y_max}')
                
                # Morocco is roughly -17° to -1° longitude, 21° to 36° latitude
                # If coordinates are outside these ranges, they're likely in a projected CRS
                needs_transform = abs(x_max) > 180 or abs(y_max) > 90
                
                if needs_transform:
                    self.stdout.write(self.style.WARNING('Coordinates appear to be in projected CRS (likely UTM or Lambert). Attempting transformation...'))
                    # Common Morocco projections: EPSG:26191 (Nord Maroc), EPSG:26192 (Sud Maroc), EPSG:26194 (Sahara)
                    # Try EPSG:26191 (Lambert Nord Maroc) -> EPSG:4326 (WGS84)
                    transformer = Transformer.from_crs("EPSG:26191", "EPSG:4326", always_xy=True)
                else:
                    # Check if coordinates are already in Morocco range
                    if x_min >= -17 and x_max <= -1 and y_min >= 21 and y_max <= 36:
                        self.stdout.write('Coordinates appear to be in Morocco lat/long (WGS84)')
                        transformer = None
                    else:
                        self.stdout.write(self.style.WARNING('Coordinates are in lat/long but not in Morocco range. May need transformation.'))
                        transformer = None
            else:
                transformer = None
            
            # Clear existing data
            ParcelPoint.objects.all().delete()
            
            # Load data
            created_count = 0
            for index, row in df.iterrows():
                try:
                    # Helper function to safely convert to float
                    def safe_float(value):
                        if pd.isna(value):
                            return None
                        try:
                            return float(value)
                        except (ValueError, TypeError):
                            return None
                    
                    # Helper function to safely convert to int
                    def safe_int(value):
                        if pd.isna(value):
                            return None
                        try:
                            return int(value)
                        except (ValueError, TypeError):
                            return None
                    
                    # Map column names to actual Excel columns
                    column_mapping = {
                        'x': 'X',
                        'y': 'Y', 
                        'parcel_id': 'ID',
                        'province': 'Province',
                        'variety': 'variety',
                        'year': 'Year',
                        'area': 'Area',
                        'yield_total': 'Yield',
                        'yield_per_ha': 'yield (t/ha)'
                    }
                    
                    # Check if columns exist, use alternative names if needed
                    def get_column_value(row, possible_names):
                        for name in possible_names:
                            if name in row.index:
                                return row[name]
                        return None
                    
                    # Get raw coordinates
                    x_raw = safe_float(get_column_value(row, ['X', 'x', 'Longitude', 'LON']))
                    y_raw = safe_float(get_column_value(row, ['Y', 'y', 'Latitude', 'LAT']))
                    
                    # Transform if needed
                    if transformer and x_raw is not None and y_raw is not None:
                        try:
                            lon, lat = transformer.transform(x_raw, y_raw)
                            # Check if transformed coordinates are in Morocco
                            if not (-17 <= lon <= -1 and 21 <= lat <= 36):
                                self.stdout.write(self.style.WARNING(f'Transformed coordinates not in Morocco for parcel {index}: lon={lon}, lat={lat}'))
                                # Try alternative CRS
                                try:
                                    transformer_alt = Transformer.from_crs("EPSG:26194", "EPSG:4326", always_xy=True)
                                    lon, lat = transformer_alt.transform(x_raw, y_raw)
                                    if not (-17 <= lon <= -1 and 21 <= lat <= 36):
                                        self.stdout.write(self.style.WARNING(f'Alternative transform also failed for parcel {index}'))
                                        continue
                                except:
                                    continue
                        except Exception as e:
                            self.stdout.write(self.style.WARNING(f'Transform failed for parcel {index}: {e}'))
                            continue
                    else:
                        lon, lat = x_raw, y_raw
                        # Check if coordinates are in Morocco range
                        if lon is not None and lat is not None and not (-17 <= lon <= -1 and 21 <= lat <= 36):
                            self.stdout.write(self.style.WARNING(f'Coordinates not in Morocco range for parcel {index}: lon={lon}, lat={lat}'))
                            continue
                    
                    parcel = ParcelPoint.objects.create(
                        x=lon,
                        y=lat,
                        parcel_id=str(get_column_value(row, ['ID', 'id', 'Parcel_ID', 'ParcelID'])) or f'Parcel_{index}',
                        province=str(get_column_value(row, ['Province', 'province', 'PROVINCE'])) or 'Unknown',
                        variety=str(get_column_value(row, ['variety', 'Variety', 'VARIETY', 'Variety_planted'])) or 'Unknown',
                        year=safe_int(get_column_value(row, ['Year', 'year', 'YEAR'])),
                        area=safe_float(get_column_value(row, ['Area', 'area', 'AREA', 'Area_ha'])),
                        yield_total=safe_float(get_column_value(row, ['Yield', 'yield', 'YIELD', 'Total_Yield'])),
                        yield_per_ha=safe_float(get_column_value(row, ['yield (t/ha)', 'Yield (t/ha)', 'yield_t_ha', 'Yield_t_ha', 'yield_per_ha']))
                    )
                    created_count += 1
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'Error creating parcel {index}: {e}'))
                    continue
            
            self.stdout.write(self.style.SUCCESS(f'Successfully loaded {created_count} parcel points'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error loading file: {e}'))
