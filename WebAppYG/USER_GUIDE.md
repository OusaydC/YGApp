# 🌾 Morocco Yield Gap Web Application - Complete User Guide

## 🚀 Quick Start

### For First Time Users:
1. Open Command Prompt/PowerShell in the `WebAppYG` folder
2. Run: `conda activate WebAppYG`
3. Run: `RUN.bat`
4. Open browser and go to: `http://127.0.0.1:8000/`

### For Subsequent Uses:
- Just run steps 2-4 above

---

## 📊 Understanding the Data

### Yield Levels (Displayed in GREEN)
These represent different production scenarios:

| Metric | Symbol | Description | Meaning |
|--------|--------|-------------|---------|
| **Actual Yield** | Ya | Real observed farmer yields | What farmers actually achieve |
| **Potential Yield** | Yp | Maximum achievable yield | Theoretical maximum under perfect conditions |
| **Water Limited Yield** | Yw | Yield under water constraints | Maximum with current rainfall/irrigation |
| **Nutrient Limited Yield** | Ynutrient | Yield with optimal nutrients | Maximum with perfect fertilization |
| **Unfertilized Yield** | Ynf | Baseline without fertilizers | Production without any fertilizer |

> 💡 **Tip**: Higher values (darker green) indicate better performance

### Yield Gap Components (Displayed in RED)
These show where production is being lost:

| Gap Type | Formula | What It Shows |
|----------|---------|---------------|
| **Total Exploitable Gap** | Yp - Ya | Overall potential for improvement |
| **Water Limitation Gap** | Yp - Yw | How much water shortage costs |
| **Nutrient Limitation Gap** | Yw - Ynutrient | How much nutrient deficiency costs |
| **Management Gap** | Ynutrient - Ya | How much poor practices cost |
| **Fertilizer Response Gap** | Ya - Ynf | How much fertilizer helps |
| **Yield Gap %** | (Yp - Ya) / Yp × 100 | Percentage of potential lost |

> 💡 **Tip**: Lower values (lighter red) indicate better performance

---

## 🗺️ Using the Interactive Map

### Basic Controls

#### 1. **Year Selection**
- **2019, 2020, 2021**: View specific year data
- **Average** ⭐ (Default): See mean values across all years
- Use **← → arrow keys** to navigate through years

#### 2. **Metric Selection**
Choose from dropdown to visualize:
- Any yield level (green scale)
- Any yield gap component (red scale)

#### 3. **Map Layers**
Toggle visibility:
- ☑️ **Communes**: Municipal boundaries
- ☑️ **Provinces**: Provincial boundaries  
- ☑️ **Regions**: Regional boundaries
- ☑️ **Parcels**: Individual field points

### Interactive Features

#### Clicking on Provinces
- Shows detailed popup with ALL metrics
- Displays province-specific statistics
- Shows breakdown of yields and gaps

#### Hovering
- Quick preview of selected metric
- Province name displayed

---

## 🎯 Actions Panel Features

### 1. **Export Map (PNG)** 📸
- **Button**: Click "Export Map (PNG)"
- **Keyboard**: Press `E` key
- **Output**: High-quality image file
- **Filename**: Auto-named with metric and year
- **Use Case**: Presentations, reports, publications

### 2. **Export Data (CSV)** 💾
- **Button**: Click "Export Data (CSV)"
- **Output**: Spreadsheet with all data
- **Filters**: Respects current crop/year selection
- **Use Case**: Statistical analysis, further processing

### 3. **Reset View** 🔄
- **Button**: Click "Reset View"
- **Keyboard**: Press `R` key
- **Action**: Returns to default map position, Average year, default metric

### 4. **Help** ❓
- **Button**: Click "Help"
- **Keyboard**: Press `H` key
- **Action**: Shows comprehensive in-app help guide

---

## ⌨️ Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `H` | Show help dialog |
| `R` | Reset map view to default |
| `E` | Export current map as PNG |
| `←` | Previous year |
| `→` | Next year |
| `ESC` | Close province details panel |

> 💡 **Pro Tip**: Press `H` anytime to see this list in-app!

---

## 📈 Understanding the Values

### Units
- **All yields**: Expressed in **t/ha** (tons per hectare)
- **Yield gap %**: Expressed in **percentage** (%)

### Typical Ranges for Moroccan Wheat
- **Actual Yield**: 1.5 - 4.0 t/ha
- **Potential Yield**: 4.0 - 8.0 t/ha
- **Yield Gaps**: 1.0 - 5.0 t/ha
- **Yield Gap %**: 30% - 70%

### Color Coding
- **Green Scale** (Yields): Lighter → Darker = Lower → Higher
- **Red Scale** (Gaps): Lighter → Darker = Lower → Higher losses

---

## 📊 Data Visualization Panel

### Yield Distribution Chart
- Located in sidebar below province information
- Shows distribution of selected metric across provinces
- Updates automatically when changing year/metric

---

## 🎓 Scientific Background

### Methodology
Based on established protocols:
- **Lobell et al. (2009)**: Climate trends and crop production
- **van Wart et al. (2013)**: Yield gap analysis framework
- **Sadras et al. (2015)**: Crop yield gaps analysis

### Data Collection
- **Period**: 2019-2021
- **Crop**: Wheat (Triticum aestivum)
- **Coverage**: Multiple provinces across Morocco
- **Method**: Plot-level field measurements and simulations

### Gap Decomposition Logic
```
Potential Yield (Yp)
    ↓ [Water Limitation]
Water Limited Yield (Yw)
    ↓ [Nutrient Limitation]
Nutrient Limited Yield
    ↓ [Management Issues]
Actual Yield (Ya)
    ↓ [Fertilizer Effect]
Unfertilized Yield (Ynf)
```

---

## 💡 Use Cases & Examples

### For Researchers
1. **Comparative Analysis**: Export CSV for statistical testing
2. **Publication Figures**: Export PNG at different metrics
3. **Trend Analysis**: Compare years 2019-2021
4. **Spatial Patterns**: Identify high/low performing regions

### For Policy Makers
1. **Intervention Targeting**: Identify provinces with largest gaps
2. **Resource Allocation**: Prioritize based on gap components
3. **Impact Assessment**: Compare years to see trends
4. **Report Generation**: Export maps for presentations

### For Agricultural Extension
1. **Farmer Training**: Show potential vs actual yields
2. **Best Practices**: Identify well-performing regions
3. **Input Recommendations**: Use gap decomposition to advise
4. **Demonstration Sites**: Target high management gap areas

---

## 🐛 Troubleshooting

### Problem: Map not loading
**Solution**: 
- Check internet connection (needs to load map tiles)
- Refresh page (F5)
- Clear browser cache

### Problem: No data showing
**Solution**:
- Verify data was loaded: Check terminal for "Successfully loaded X records"
- Re-run: `python manage.py load_real_data`

### Problem: Export not working
**Solution**:
- **PNG Export**: Try browser print function (Ctrl+P → Save as PDF)
- **CSV Export**: Check browser's download folder
- Ensure pop-ups are not blocked

### Problem: Slow performance
**Solution**:
- Hide parcel layer if not needed
- Use single year instead of switching frequently
- Close other browser tabs

---

## 📁 File Structure Reference

```
WebAppYG/
├── RUN.bat                    ← Run this to start
├── manage.py                  ← Django management
├── data/
│   ├── plot_v_p.xlsx         ← Source data
│   ├── Morocco_shapefiles/   ← Province boundaries
│   └── inst.txt              ← Quick reference
├── templates/
│   └── map.html              ← Main application
└── core/
    ├── models.py             ← Database structure
    └── management/commands/
        └── load_real_data.py ← Data loading script
```

---

## 🔄 Updating Data

### To Load New Data:
1. Replace `data/plot_v_p.xlsx` with new file
2. Keep same column structure
3. Run: `python manage.py load_real_data`
4. Restart server

### Required Columns in Excel:
- Province
- Year
- Crop
- Yield_Observed
- Yield_Potential
- Yield_Water_Limited
- Yield_Nutrient_Limited
- Yield_Unfertilized

---

## 📞 Support

### Documentation
- **This Guide**: `USER_GUIDE.md`
- **Improvements List**: `IMPROVEMENTS_SUMMARY.md`
- **Quick Reference**: `data/inst.txt`

### In-App Help
- Press `H` key anytime
- Click "Help" button in Actions panel

---

## 🎯 Best Practices

### For Presentations
1. Set to "Average" year for overall trends
2. Export at "Total Exploitable Gap" metric
3. Use reset view before exporting
4. Keep legend visible

### For Analysis
1. Start with "Yield Gap %" to identify priorities
2. Then decompose using gap components
3. Export CSV for statistical testing
4. Compare years to identify trends

### For Reports
1. Export PNG for each key metric
2. Use consistent year (Average recommended)
3. Include legend in screenshots
4. Document methodology (see Scientific Background)

---

## 🆕 Latest Features (v2.0)

✅ PNG map export with automatic naming  
✅ Complete yield gap decomposition (5 components)  
✅ Keyboard shortcuts for efficiency  
✅ In-app help system  
✅ Reset view function  
✅ Print-friendly layout  
✅ Enhanced legend with proper labeling  
✅ Average year calculation  
✅ Improved data accuracy (proper unit conversion)  

---

## 📝 Citation

If using this tool in research, please cite:

```
Morocco Yield Gap Analysis Web Application (2025)
Data Source: Plot-level wheat trials, Morocco (2019-2021)
Methodology: Based on van Wart et al. (2013) yield gap framework
```

---

**Version**: 2.0  
**Last Updated**: December 2025  
**Status**: Production Ready ✅  
**Developed for**: Agricultural yield gap research and policy support

---

## 🌟 Quick Tips Summary

1. 📊 Use **Average** year for overall trends
2. 🎨 **Green = yields** (higher better), **Red = gaps** (lower better)
3. ⌨️ Press **H** anytime for help
4. 📸 Press **E** to export map quickly
5. 🔄 Press **R** to reset view
6. 📁 Export **PNG** for presentations, **CSV** for analysis
7. 🗺️ Click provinces for detailed breakdown
8. ⬅️➡️ Use arrow keys to navigate years
9. 📈 Check charts in sidebar for distributions
10. 💾 All data in **t/ha** (tons per hectare)

---

**Happy Mapping! 🌾📊**


