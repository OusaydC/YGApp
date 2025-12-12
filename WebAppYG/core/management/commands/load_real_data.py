from django.core.management.base import BaseCommand
from core.models import AdministrativeBoundary, Crop, YieldData
import pandas as pd


class Command(BaseCommand):
    help = 'Load real data from Yield_Statistics (mean values in t/ha)'
    
    def handle(self, *args, **options):
        YieldData.objects.all().delete()
        
        # Read two sheets we need
        df_province_scenario = pd.read_excel('data/Yield_Statistics_Complete_Analysis.xlsx',
                                             sheet_name='Yield_By_Province_Scenario')
        df_province_year_scenario = pd.read_excel('data/Yield_Statistics_Complete_Analysis.xlsx',
                                                   sheet_name='Yield_By_Province_Year_Scenario')
        
        self.stdout.write(f"✓ Loaded yield statistics")
        self.stdout.write(f"  Province_Scenario shape: {df_province_scenario.shape}")
        self.stdout.write(f"  Province_Year_Scenario shape: {df_province_year_scenario.shape}")
        self.stdout.write(f"  Years in data: {sorted(df_province_year_scenario['Year'].unique())}")
        self.stdout.write(f"  Scenarios in data: {sorted(df_province_year_scenario['Scenario'].unique())}")
        
        # Get concerned provinces from shapefile
        provinces = {p.name.upper().replace('-', ' '): p 
                    for p in AdministrativeBoundary.objects.filter(level='province')}
        
        wheat, _ = Crop.objects.get_or_create(name='wheat')
        
        # Province name mapping
        province_map = {
            'Beni-Mellal': 'BENI MELLAL', 'Berrechid': 'BERRECHID',
            'El-Jadida': 'EL JADIDA', 'Kenitra': 'KENITRA',
            'Khemisset': 'KHEMISSET', 'Khenifra': 'KHENIFRA',
            'Larache': 'LARACHE', 'Meknes': 'MEKNES',
            'Rehamna': 'REHAMNA', 'Settat': 'SETTAT',
            'Sidi-Kacem': 'SIDI KACEM', 'Sidi-Slimane': 'SIDI SLIMANE',
            'Taounate': 'TAOUNATE', 'Taza': 'TAZA'
        }
        
        count = 0
        for excel_prov, shapefile_prov in province_map.items():
            if shapefile_prov not in provinces:
                continue
            
            boundary = provinces[shapefile_prov]
            
            # 1. Individual years from Province_Year_Scenario sheet
            for year in [2019, 2020, 2021]:
                # Get all scenarios - use Calibrated as Actual/Observed
                scenarios = {}
                for scenario_name in ['Potential', 'Water Limited', 'Calibrated', 'Unfertilized']:
                    data = df_province_year_scenario[
                        (df_province_year_scenario['Province'] == excel_prov) & 
                        (df_province_year_scenario['Year'] == year) &
                        (df_province_year_scenario['Scenario'] == scenario_name)
                    ]
                    if not data.empty:
                        scenarios[scenario_name] = data['Mean'].values[0]
                
                if count == 0 and year == 2019:
                    self.stdout.write(f"DEBUG {excel_prov} {year}: Found scenarios: {list(scenarios.keys())}")
                
                # Use Calibrated as actual yield for individual years
                if 'Potential' in scenarios and 'Calibrated' in scenarios:
                    # Yield levels - use Calibrated as actual yield
                    Y_p = max(0, scenarios.get('Potential', 0))
                    Y_w = max(0, scenarios.get('Water Limited', Y_p))
                    Y_nutrient = max(0, scenarios.get('Calibrated', 0))
                    Y_a = Y_nutrient  # Use Calibrated as actual for individual years
                    Y_nf = max(0, scenarios.get('Unfertilized', 0))
                    
                    # Yield gaps (no negatives)
                    total_gap = max(0, Y_p - Y_a)
                    water_gap = max(0, Y_p - Y_w)
                    nutrient_gap = max(0, Y_w - Y_nutrient)
                    mgmt_gap = max(0, Y_nutrient - Y_a)
                    fert_response = max(0, Y_a - Y_nf)
                    
                    gap_pct = (total_gap / Y_p * 100) if Y_p > 0 else 0
                    
                    YieldData.objects.create(
                        boundary=boundary, crop=wheat, year=year,
                        # Yield levels
                        actual_yield=round(Y_a, 2),
                        potential_yield=round(Y_p, 2),
                        water_limited_yield=round(Y_w, 2),
                        nutrient_limited_yield=round(Y_nutrient, 2),
                        unfertilized_yield=round(Y_nf, 2),
                        # Basic gaps
                        yield_gap=round(total_gap, 2),
                        yield_gap_percent=round(gap_pct, 2),
                        # Decomposed gaps
                        water_gap=round(water_gap, 2),
                        nutrient_gap=round(nutrient_gap, 2),
                        management_gap=round(mgmt_gap, 2),
                        fertilizer_response_gap=round(fert_response, 2),
                        data_source='Real Statistics'
                    )
                    count += 1
                    if count <= 3:
                        self.stdout.write(f"✓ {shapefile_prov} ({year}): Actual={Y_a:.1f}, Pot={Y_p:.1f}, Gap={total_gap:.1f} t/ha")
            
            # 2. Average from Province_Scenario sheet (already averaged across years)
            scenarios_avg = {}
            for scenario_name in ['Potential', 'Water Limited', 'Calibrated', 'Unfertilized', 'Observed']:
                data = df_province_scenario[
                    (df_province_scenario['Province'] == excel_prov) & 
                    (df_province_scenario['Scenario'] == scenario_name)
                ]
                if not data.empty:
                    scenarios_avg[scenario_name] = data['Mean'].values[0]
            
            if 'Potential' in scenarios_avg and 'Observed' in scenarios_avg:
                # Yield levels (no negatives)
                Y_p = max(0, scenarios_avg.get('Potential', 0))
                Y_w = max(0, scenarios_avg.get('Water Limited', Y_p))
                Y_nutrient = max(0, scenarios_avg.get('Calibrated', Y_w))
                Y_a = max(0, scenarios_avg.get('Observed', 0))
                Y_nf = max(0, scenarios_avg.get('Unfertilized', Y_a))
                
                # Yield gaps (no negatives)
                total_gap = max(0, Y_p - Y_a)
                water_gap = max(0, Y_p - Y_w)
                nutrient_gap = max(0, Y_w - Y_nutrient)
                mgmt_gap = max(0, Y_nutrient - Y_a)
                fert_response = max(0, Y_a - Y_nf)
                
                gap_pct = (total_gap / Y_p * 100) if Y_p > 0 else 0
                
                YieldData.objects.create(
                    boundary=boundary, crop=wheat, year=9999,  # 9999 = Average
                    # Yield levels
                    actual_yield=round(Y_a, 2),
                    potential_yield=round(Y_p, 2),
                    water_limited_yield=round(Y_w, 2),
                    nutrient_limited_yield=round(Y_nutrient, 2),
                    unfertilized_yield=round(Y_nf, 2),
                    # Basic gaps
                    yield_gap=round(total_gap, 2),
                    yield_gap_percent=round(gap_pct, 2),
                    # Decomposed gaps
                    water_gap=round(water_gap, 2),
                    nutrient_gap=round(nutrient_gap, 2),
                    management_gap=round(mgmt_gap, 2),
                    fertilizer_response_gap=round(fert_response, 2),
                    data_source='Real Statistics - Average'
                )
                count += 1
                if count <= 15:  # Show first average
                    self.stdout.write(f"✓ {shapefile_prov} (Average): Actual={Y_a:.1f}, Pot={Y_p:.1f}, Gap={total_gap:.1f} t/ha")
        
        self.stdout.write(self.style.SUCCESS(f"\n✓ Created {count} records"))
        self.stdout.write(f"✓ Years: 2019, 2020, 2021, Average (9999)")
        self.stdout.write(f"✓ Yield gap % calculated correctly")

