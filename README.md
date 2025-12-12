# Morocco Yield Gap WebApp (WebAppYG)

## Phase 0 — Product Definition

### Goal (v1)
A fast, public map for Morocco showing Actual Yield, Potential/Water-Limited Yield (WLY), and Yield Gap by crop, year, and administrative area (commune/province/region), plus a detail panel and CSV export.

### Core Users
- **Researchers**: Academic and institutional researchers studying agricultural productivity
- **Extension agents**: Agricultural advisors working with farmers
- **Policymakers**: Government officials making agricultural policy decisions
- **Growers**: Farmers and agricultural producers

### User Stories

#### Primary Features (v1)
1. **As a user**, I can pick crop (e.g., wheat, barley), year, and metric (actual, potential, gap t/ha, gap %) and see a choropleth map
2. **As a user**, clicking an area opens a panel with time series (10–20 years), summary stats, and download options
3. **As a user**, I can export data as CSV for further analysis

#### Optional Features (v1.1)
- **"Compare My Farm"**: Enter field yield to benchmark against local distribution/potential

### Scope Guardrails
- v1 uses administrative polygons, not 1-km grids (add later)
- Potential yield = water-limited (rainfed) via one chosen approach
- Process-based modeling to be added later

### Technical Stack
- **Backend**: Django 5, GeoDjango, Django REST Framework (DRF)
- **Database**: PostgreSQL 16 + PostGIS
- **Cache/Tasks**: Redis + Celery (ETL & heavy calculations)
- **Frontend**: Leaflet (fast to ship), vanilla or Alpine.js
- **Tiling**: Vector tiles with t_rex/Tegola or Tippecanoe + Tileserver-GL (later)
- **Deploy**: Docker, docker-compose, Nginx, Let's Encrypt

## Project Structure
```
yg_ma/
├── core/           # Models for boundaries, yields, metadata
├── api/            # Django REST Framework endpoints
├── etl/            # Management commands for data processing
├── frontend/       # Static files, templates
└── config/         # Settings, URLs, deployment configs
```


