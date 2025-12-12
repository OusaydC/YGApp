# WebAppYG - Setup and Run Instructions

## Quick Start Commands

### First Time Setup (Complete Installation)
```bash
cd "C:\Users\Lahcen.OUSAYD\OneDrive - Université Mohammed VI Polytechnique\Bureau\M3\WebApp\WebAppYG"
conda activate WebAppYG
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

# Load all shapefiles and data
python manage.py load_shapefiles --shapefile "data/Shapefiles/Morocco.shp" --level "country" --name-field "NAME" --code-field "CODE"
python manage.py load_shapefiles --shapefile "data/Shapefiles/Concerned_Provinces.shp" --level "province" --name-field "NOM_PROV" --code-field "CODE_PROVI"
python manage.py load_variety_shapefiles --dir "data/Shapefiles/Varieties"
python manage.py create_sample_data
python manage.py runserver
```

### Daily Use (Every Time You Launch the App)
```bash
cd "C:\Users\Lahcen.OUSAYD\OneDrive - Université Mohammed VI Polytechnique\Bureau\M3\WebApp\WebAppYG"
conda activate WebAppYG
python manage.py runserver
```

**Access the application:**
- Open browser and go to: `http://127.0.0.1:8000`
- The application will load with:
  - Morocco country boundary
  - All concerned provinces with yield data
  - Parcel points with variety information
  - Interactive map with colored regions

### After Code Changes
```bash
cd "C:\Users\Lahcen.OUSAYD\OneDrive - Université Mohammed VI Polytechnique\Bureau\M3\WebApp\WebAppYG"
conda activate WebAppYG
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## Access the Application

- **Main Application**: `http://127.0.0.1:8000`
- **Admin Interface**: `http://127.0.0.1:8000/admin`

## Stop the Server

- Press `Ctrl + C` in the command prompt

## Data Management

### Reload Sample Data
```bash
python manage.py create_sample_data
```

### Load Shapefiles (Complete Setup)
```bash
# Load Morocco country boundary
python manage.py load_shapefiles --shapefile "data/Shapefiles/Morocco.shp" --level "country" --name-field "NAME" --code-field "CODE"

# Load concerned provinces
python manage.py load_shapefiles --shapefile "data/Shapefiles/Concerned_Provinces.shp" --level "province" --name-field "NOM_PROV" --code-field "CODE_PROVI"

# Load variety shapefiles (parcel points)
python manage.py load_variety_shapefiles --dir "data/Shapefiles/Varieties"

# Create yield data for all loaded provinces
python manage.py create_sample_data
```

### Clear and Reload All Data (Complete Reset)
```bash
# Stop server first (Ctrl + C)
cd "C:\Users\Lahcen.OUSAYD\OneDrive - Université Mohammed VI Polytechnique\Bureau\M3\WebApp\WebAppYG"
conda activate WebAppYG
python manage.py shell
# Then in Python shell:
from core.models import *
AdministrativeBoundary.objects.all().delete()
YieldData.objects.all().delete()
ParcelPoint.objects.all().delete()
Crop.objects.all().delete()
exit()

# Reload all data
python manage.py load_shapefiles --shapefile "data/Shapefiles/Morocco.shp" --level "country" --name-field "NAME" --code-field "CODE"
python manage.py load_shapefiles --shapefile "data/Shapefiles/Concerned_Provinces.shp" --level "province" --name-field "NOM_PROV" --code-field "CODE_PROVI"
python manage.py load_variety_shapefiles --dir "data/Shapefiles/Varieties"
python manage.py create_sample_data
python manage.py runserver
```

## Migration Commands

### Check Migration Status
```bash
python manage.py showmigrations
```

### Create Migrations
```bash
python manage.py makemigrations
```

### Apply Migrations
```bash
python manage.py migrate
```

### Complete Database Reset
```bash
# Delete database
del db.sqlite3

# Delete migration files
del core\migrations\*.py
# Keep __init__.py

# Recreate everything
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py create_sample_data
python manage.py runserver
```

## Troubleshooting

### Common Issues

1. **Conda not found**
   ```bash
   C:\Users\Lahcen.OUSAYD\AppData\Local\anaconda3\Scripts\conda.exe activate WebAppYG
   ```

2. **Python not found**
   ```bash
   C:\Users\Lahcen.OUSAYD\AppData\Local\anaconda3\envs\WebAppYG\python.exe manage.py runserver
   ```

3. **Port already in use**
   ```bash
   python manage.py runserver 8001
   ```

4. **Database locked**
   - Stop the server first (Ctrl + C)
   - Then run migration commands

### Environment Variables (if needed)
```bash
set GEOS_LIBRARY_PATH=C:\Users\Lahcen.OUSAYD\AppData\Local\anaconda3\envs\WebAppYG\Library\bin\geos_c.dll
set GDAL_LIBRARY_PATH=C:\Users\Lahcen.OUSAYD\AppData\Local\anaconda3\envs\WebAppYG\Library\bin\gdal304.dll
set PROJ_LIB=C:\Users\Lahcen.OUSAYD\AppData\Local\anaconda3\envs\WebAppYG\Library\share\proj
```

## Application Features

### Main Features
- Interactive map with Morocco country boundary and concerned provinces
- Yield data visualization (Actual, Potential, Yield Gap) with colored regions
- Parcel-level monitoring with variety information
- Publications page with research papers
- Professional agricultural monitoring interface

### Map Controls
- Regional Analysis: View yield data by concerned provinces
- Parcel Analysis: View individual parcel points with variety data
- Metric selection: Actual Yield, Potential Yield, Yield Gap
- Crop selection: Wheat, Barley, Maize
- Year selection: 2018-2025

### Satellite Integration
- Click on parcel points to open geojson.io
- High-resolution satellite imagery
- Direct zoom to parcel location
- GeoJSON point visualization

### Data Sources
- Morocco country boundary: `data/Shapefiles/Morocco.shp`
- Concerned provinces: `data/Shapefiles/Concerned_Provinces.shp`
- Variety data: `data/Shapefiles/Varieties/` (Achtar.shp, etc.)

## File Structure
```
WebAppYG/
├── core/                    # Main Django app
│   ├── models.py           # Database models
│   ├── views.py            # API endpoints
│   ├── admin.py            # Admin interface
│   └── management/commands/ # Custom commands
├── api/                    # API app
├── templates/              # HTML templates
│   └── map.html           # Main application template
├── data/                   # Data files
│   └── Shapefiles/        # Shapefile data
├── manage.py              # Django management script
└── requirements.txt       # Python dependencies
```

## Support

For issues or questions:
1. Check the console output for error messages
2. Verify all dependencies are installed
3. Ensure conda environment is activated
4. Check file permissions
5. Restart the server if needed

## Version Information
- Django: 4.2.24
- Python: 3.13
- Database: SQLite (development)
- Frontend: Leaflet.js, Vanilla JavaScript
- Styling: CSS3, Flexbox, Grid

---
*Generated: $(date)*
*WebAppYG - Pan Moroccan Yield & Precipitation Gaps Platform*
