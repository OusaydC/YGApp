from django.db import models

class AdministrativeBoundary(models.Model):
    name = models.CharField(max_length=200)
    level = models.CharField(max_length=50)  # commune, province, region
    code = models.CharField(max_length=20, unique=True)
    geometry_json = models.TextField(blank=True, null=True)  # Store GeoJSON as text
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Administrative Boundaries"

class Crop(models.Model):
    name = models.CharField(max_length=100, unique=True)
    scientific_name = models.CharField(max_length=200, blank=True)
    
    def __str__(self):
        return self.name

class YieldData(models.Model):
    boundary = models.ForeignKey(AdministrativeBoundary, on_delete=models.CASCADE)
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    year = models.IntegerField()
    
    # Yield levels (t/ha)
    actual_yield = models.FloatField(null=True, blank=True)  # Y_a - Observed
    potential_yield = models.FloatField(null=True, blank=True)  # Y_p - Potential
    water_limited_yield = models.FloatField(null=True, blank=True)  # Y_w - Water Limited
    nutrient_limited_yield = models.FloatField(null=True, blank=True)  # Y_nutrient - Calibrated
    unfertilized_yield = models.FloatField(null=True, blank=True)  # Y_nf - Unfertilized
    
    # Basic gaps (t/ha)
    yield_gap = models.FloatField(null=True, blank=True)  # Total exploitable: Y_p - Y_a
    yield_gap_percent = models.FloatField(null=True, blank=True)  # %
    
    # Decomposed yield gaps (t/ha) - Lobell et al., 2009
    water_gap = models.FloatField(null=True, blank=True)  # ∆Y_w = Y_p - Y_w
    nutrient_gap = models.FloatField(null=True, blank=True)  # ∆Y_nut = Y_w - Y_nutrient
    management_gap = models.FloatField(null=True, blank=True)  # ∆Y_mgmt = Y_nutrient - Y_a
    fertilizer_response_gap = models.FloatField(null=True, blank=True)  # ∆Y_f = Y_a - Y_nf
    
    data_source = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['boundary', 'crop', 'year']

class ParcelPoint(models.Model):
    parcel_id = models.CharField(max_length=100, unique=True)
    province = models.CharField(max_length=100)
    variety = models.CharField(max_length=100)
    year = models.IntegerField()
    yield_per_ha = models.FloatField(null=True, blank=True)
    yield_total = models.FloatField(null=True, blank=True)
    area = models.FloatField(null=True, blank=True)
    x = models.FloatField()  # longitude
    y = models.FloatField()  # latitude
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Parcel Points"


class Variety(models.Model):
    """Wheat varieties"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Varieties"


class Scenario(models.Model):
    """Yield scenarios"""
    SCENARIO_CHOICES = [
        ('Potential', 'Potential'),
        ('Water Limited', 'Water Limited'),
        ('Calibrated', 'Calibrated'),
        ('Unfertilized', 'Unfertilized'),
        ('Sowing Date', 'Sowing Date'),
        ('Observed', 'Observed'),
    ]
    
    name = models.CharField(max_length=100, unique=True, choices=SCENARIO_CHOICES)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name


class YieldStatistics(models.Model):
    """Statistical data for yields by variety, province, year, and scenario"""
    variety = models.ForeignKey(Variety, on_delete=models.CASCADE, null=True, blank=True)
    province = models.CharField(max_length=100, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE, null=True, blank=True)
    
    # Statistical measures (all in t/ha)
    count = models.IntegerField()
    mean = models.FloatField()
    std = models.FloatField(null=True, blank=True)
    min = models.FloatField(null=True, blank=True)
    q25 = models.FloatField(null=True, blank=True)
    median = models.FloatField(null=True, blank=True)
    q75 = models.FloatField(null=True, blank=True)
    max = models.FloatField(null=True, blank=True)
    
    data_source = models.CharField(max_length=200, default='Excel Import')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Yield Statistics"
        indexes = [
            models.Index(fields=['variety', 'province', 'year', 'scenario']),
            models.Index(fields=['province', 'year']),
            models.Index(fields=['variety', 'year']),
        ]
    
    def __str__(self):
        parts = []
        if self.variety:
            parts.append(str(self.variety))
        if self.province:
            parts.append(self.province)
        if self.year:
            parts.append(str(self.year))
        if self.scenario:
            parts.append(str(self.scenario))
        return ' - '.join(parts) if parts else 'Overall Statistics'


class GapType(models.Model):
    """Types of yield gaps"""
    GAP_CHOICES = [
        ('Total Exploitable Yield Gap', 'Total Exploitable Yield Gap'),
        ('Water Limitation Gap', 'Water Limitation Gap'),
        ('Calibrated vs Water Limited Gap', 'Calibrated vs Water Limited Gap'),
        ('Fertilizer Response Gap', 'Fertilizer Response Gap'),
        ('Sowing Date Impact Gap', 'Sowing Date Impact Gap'),
    ]
    
    name = models.CharField(max_length=100, unique=True, choices=GAP_CHOICES)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name


class GapStatistics(models.Model):
    """Statistical data for yield gaps"""
    gap_type = models.ForeignKey(GapType, on_delete=models.CASCADE, null=True, blank=True)
    variety = models.ForeignKey(Variety, on_delete=models.CASCADE, null=True, blank=True)
    province = models.CharField(max_length=100, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    
    # Statistical measures (all in t/ha)
    count = models.IntegerField()
    mean = models.FloatField()
    std = models.FloatField(null=True, blank=True)
    min = models.FloatField(null=True, blank=True)
    q25 = models.FloatField(null=True, blank=True)
    median = models.FloatField(null=True, blank=True)
    q75 = models.FloatField(null=True, blank=True)
    max = models.FloatField(null=True, blank=True)
    
    data_source = models.CharField(max_length=200, default='Excel Import')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Gap Statistics"
        indexes = [
            models.Index(fields=['gap_type', 'variety', 'province', 'year']),
            models.Index(fields=['province', 'year']),
            models.Index(fields=['variety', 'year']),
        ]
    
    def __str__(self):
        parts = []
        if self.gap_type:
            parts.append(str(self.gap_type))
        if self.variety:
            parts.append(str(self.variety))
        if self.province:
            parts.append(self.province)
        if self.year:
            parts.append(str(self.year))
        return ' - '.join(parts) if parts else 'Overall Gap Statistics'