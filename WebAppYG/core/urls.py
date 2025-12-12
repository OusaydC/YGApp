from django.urls import path
from . import views

urlpatterns = [
    path('', views.map_view, name='map'),
    path('api/yield-data/', views.api_yield_data, name='yield_data_api'),
    path('api/boundaries/', views.api_boundaries, name='boundaries_api'),
    path('api/crops/', views.api_crops, name='crops_api'),
    path('api/years/', views.api_years, name='years_api'),
    path('api/export-csv/', views.export_csv, name='export_csv'),
]