#!/usr/bin/env python
"""
Startup script to ensure data is loaded on Render
This runs before Gunicorn starts
"""
import os
import sys
from pathlib import Path

# Add project root to path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yg_ma.settings')
django.setup()

from django.core.management import call_command
from django.conf import settings
from core.models import AdministrativeBoundary, YieldData

def verify_files_exist():
    """Verify all required data files exist"""
    print("\n" + "=" * 60)
    print("Verifying data files exist...")
    print("=" * 60)
    
    base_dir = Path(settings.BASE_DIR)
    files_to_check = [
        base_dir / 'data' / 'Shapefiles' / 'Morocco' / 'Morocco.shp',
        base_dir / 'data' / 'Shapefiles' / 'Concerned_Provinces.shp',
        base_dir / 'data' / 'Yield_Statistics_Complete_Analysis.xlsx',
    ]
    
    all_exist = True
    for file_path in files_to_check:
        exists = file_path.exists()
        status = "✓" if exists else "✗"
        print(f"{status} {file_path}")
        if not exists:
            all_exist = False
            # Try to find it
            if file_path.parent.exists():
                print(f"   Directory exists. Files in directory:")
                for f in file_path.parent.iterdir():
                    print(f"     - {f.name}")
    
    print("=" * 60)
    return all_exist

def check_and_load_data():
    """Check if data exists, if not, load it"""
    print("\n" + "=" * 60)
    print("Checking if data is loaded...")
    print("=" * 60)
    
    # Verify files exist first
    if not verify_files_exist():
        print("\n⚠️  WARNING: Some data files are missing!")
        print("   Data loading may fail. Check file paths above.")
    
    # Check if data exists
    try:
        boundary_count = AdministrativeBoundary.objects.count()
        yield_count = YieldData.objects.count()
        print(f"\nCurrent data: {boundary_count} boundaries, {yield_count} yield records")
    except Exception as e:
        print(f"\n⚠️  Error checking database: {e}")
        print("   Database might not be initialized. Will try to load data anyway.")
        boundary_count = 0
        yield_count = 0
    
    if boundary_count == 0 or yield_count == 0:
        print("\n⚠️  Data missing! Loading data now...")
        print("=" * 60)
        
        base_dir = Path(settings.BASE_DIR)
        success_count = 0
        fail_count = 0
        
        # 1. Load Morocco
        print("\n[1/4] Loading Morocco shapefile...")
        morocco_path = base_dir / 'data' / 'Shapefiles' / 'Morocco' / 'Morocco.shp'
        try:
            if morocco_path.exists():
                call_command('load_shapefiles', shapefile=str(morocco_path), verbosity=2)
                print("   ✓ Morocco loaded successfully")
                success_count += 1
            else:
                print(f"   ✗ File not found: {morocco_path}")
                fail_count += 1
        except Exception as e:
            print(f"   ✗ Morocco failed: {e}")
            import traceback
            traceback.print_exc()
            fail_count += 1
        
        # 2. Load Provinces
        print("\n[2/4] Loading Provinces shapefile...")
        provinces_path = base_dir / 'data' / 'Shapefiles' / 'Concerned_Provinces.shp'
        try:
            if provinces_path.exists():
                call_command('load_shapefiles', shapefile=str(provinces_path), verbosity=2)
                print("   ✓ Provinces loaded successfully")
                success_count += 1
            else:
                print(f"   ✗ File not found: {provinces_path}")
                fail_count += 1
        except Exception as e:
            print(f"   ✗ Provinces failed: {e}")
            import traceback
            traceback.print_exc()
            fail_count += 1
        
        # 3. Load Varieties
        print("\n[3/4] Loading Variety shapefiles...")
        try:
            call_command('load_variety_shapefiles', verbosity=2)
            print("   ✓ Varieties loaded successfully")
            success_count += 1
        except Exception as e:
            print(f"   ✗ Varieties failed: {e}")
            import traceback
            traceback.print_exc()
            fail_count += 1
        
        # 4. Load Yield Data
        print("\n[4/4] Loading Yield data...")
        yield_file = base_dir / 'data' / 'Yield_Statistics_Complete_Analysis.xlsx'
        try:
            if yield_file.exists():
                call_command('load_real_data', verbosity=2)
                print("   ✓ Yield data loaded successfully")
                success_count += 1
            else:
                print(f"   ✗ File not found: {yield_file}")
                fail_count += 1
        except Exception as e:
            print(f"   ✗ Yield data failed: {e}")
            import traceback
            traceback.print_exc()
            fail_count += 1
        
        # Final verification
        print("\n" + "=" * 60)
        print("Final verification...")
        print("=" * 60)
        try:
            boundary_count = AdministrativeBoundary.objects.count()
            yield_count = YieldData.objects.count()
            print(f"✅ Final data: {boundary_count} boundaries, {yield_count} yield records")
            print(f"✅ Successfully loaded: {success_count}/4")
            if fail_count > 0:
                print(f"⚠️  Failed: {fail_count}/4")
        except Exception as e:
            print(f"❌ Error verifying data: {e}")
    else:
        print("✅ Data already loaded!")
    
    print("=" * 60 + "\n")

if __name__ == '__main__':
    check_and_load_data()

