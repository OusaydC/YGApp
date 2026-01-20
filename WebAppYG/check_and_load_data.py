#!/usr/bin/env python
"""
Startup script to ensure data is loaded on Render
This runs before Gunicorn starts
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yg_ma.settings')
django.setup()

from django.core.management import call_command
from core.models import AdministrativeBoundary, YieldData

def check_and_load_data():
    """Check if data exists, if not, load it"""
    print("=" * 60)
    print("Checking if data is loaded...")
    print("=" * 60)
    
    # Check if data exists
    boundary_count = AdministrativeBoundary.objects.count()
    yield_count = YieldData.objects.count()
    
    print(f"Current data: {boundary_count} boundaries, {yield_count} yield records")
    
    if boundary_count == 0 or yield_count == 0:
        print("\n⚠️  Data missing! Loading data now...")
        print("=" * 60)
        
        try:
            # 1. Load Morocco
            print("\n1. Loading Morocco shapefile...")
            try:
                call_command('load_shapefiles', shapefile='data/Shapefiles/Morocco/Morocco.shp', verbosity=2)
                print("   ✓ Morocco loaded")
            except Exception as e:
                print(f"   ✗ Morocco failed: {e}")
            
            # 2. Load Provinces
            print("\n2. Loading Provinces shapefile...")
            try:
                call_command('load_shapefiles', shapefile='data/Shapefiles/Concerned_Provinces.shp', verbosity=2)
                print("   ✓ Provinces loaded")
            except Exception as e:
                print(f"   ✗ Provinces failed: {e}")
            
            # 3. Load Varieties
            print("\n3. Loading Variety shapefiles...")
            try:
                call_command('load_variety_shapefiles', verbosity=2)
                print("   ✓ Varieties loaded")
            except Exception as e:
                print(f"   ✗ Varieties failed: {e}")
            
            # 4. Load Yield Data
            print("\n4. Loading Yield data...")
            try:
                call_command('load_real_data', verbosity=2)
                print("   ✓ Yield data loaded")
            except Exception as e:
                print(f"   ✗ Yield data failed: {e}")
            
            # Verify
            boundary_count = AdministrativeBoundary.objects.count()
            yield_count = YieldData.objects.count()
            print(f"\n✅ Final data: {boundary_count} boundaries, {yield_count} yield records")
            
        except Exception as e:
            print(f"\n❌ Error loading data: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("✅ Data already loaded!")
    
    print("=" * 60)

if __name__ == '__main__':
    check_and_load_data()

