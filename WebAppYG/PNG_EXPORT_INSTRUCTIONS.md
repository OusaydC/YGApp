# 📸 PNG Export Instructions

## Fixed Issues

### ✅ What Was Fixed:

1. **Export Format**: Now exports as `.png` file (not PDF)
2. **Color Bar**: Legend colors now display correctly (no longer white)
3. **Cropping**: Map automatically cropped to Morocco bounds only
4. **Quality**: High-quality PNG suitable for publications

---

## How to Use PNG Export

### Method 1: Button Click
1. Select your desired **Year** and **Metric**
2. Click **"Export Map (PNG)"** button in Actions panel
3. Wait for notification: "Preparing map export..."
4. File downloads automatically as `.png`

### Method 2: Keyboard Shortcut ⚡
1. Select your desired **Year** and **Metric**
2. Press **E** key
3. File downloads automatically

---

## What Gets Exported

The PNG file includes:

✅ **Title**: "Morocco Wheat Yield Gap Analysis"
✅ **Subtitle**: Metric name and year
✅ **Map**: Cropped to Morocco boundaries only (no empty space)
✅ **Legend**: Full color bar with values and units
✅ **Border**: Clean border around map
✅ **Source**: Attribution at bottom

❌ **Excluded**: Sidebars, controls, navigation, buttons

---

## Technical Details

### File Specifications:
- **Format**: PNG (image/png)
- **Quality**: High resolution (matches screen)
- **Filename**: Auto-generated: `Morocco_YieldGap_[Metric]_[Year].png`
- **Background**: White
- **Colors**: Full RGB color preservation

### Morocco Bounds:
- **Latitude**: 21°N to 36°N
- **Longitude**: 17°W to 1°W
- **Padding**: 40 pixels around boundaries

### Canvas Composition:
1. **Title Section**: 100px height
2. **Map Section**: Cropped to Morocco with 40px padding
3. **Legend Section**: 250px width on right side
4. **Margins**: 40px on all sides

---

## Troubleshooting

### Issue: File downloads as PDF or WebP
**Cause**: Browser might change format
**Solution**:
1. Check your browser's download settings
2. Use Chrome or Firefox (best compatibility)
3. If file has wrong extension, rename to `.png`

### Issue: Colors still appear white
**Cause**: Legend not fully loaded when export triggered
**Solution**:
1. Wait 2-3 seconds after changing metric
2. Let map fully render before exporting
3. Refresh page if issue persists

### Issue: Map shows too much empty space
**Cause**: Zoom level too far out
**Solution**:
1. The export auto-crops to Morocco bounds
2. If still showing extra space, zoom in slightly first
3. Then export (bounds are calculated automatically)

### Issue: Legend values are cut off
**Cause**: Very large numbers
**Solution**: This should be auto-handled, but report if you see this

### Issue: Export notification says "failed"
**Cause**: Browser compatibility
**Fallback**:
1. Use alternative export: Press `Ctrl+P` to print
2. Select "Save as PDF" or "Print to PDF"
3. Or use Windows Snipping Tool for manual capture

---

## Best Practices

### For Publications:
1. ✅ Use **Average** year for overall trends
2. ✅ Export at full screen for best quality
3. ✅ Choose appropriate metric for your message
4. ✅ File is publication-ready (white background, clean layout)

### For Presentations:
1. ✅ Export multiple metrics for comparison
2. ✅ Filename includes metric and year for organization
3. ✅ Use descriptive metric names (already included)
4. ✅ Legend shows appropriate units (t/ha or %)

### For Reports:
1. ✅ Export series for each year (2019-2025)
2. ✅ Compare same metric across years
3. ✅ Include source attribution (auto-added)
4. ✅ White background works for all document types

---

## Alternative Export Methods

### If PNG Export Doesn't Work:

#### Method A: Browser Print to PDF
```
1. Press Ctrl+P (Windows) or Cmd+P (Mac)
2. Select "Save as PDF" or "Microsoft Print to PDF"
3. Save file
4. Convert PDF to PNG using online tool or:
   - Adobe Acrobat
   - GIMP
   - Photoshop
```

#### Method B: Screenshot Tool
```
Windows:
1. Press Windows+Shift+S
2. Select area to capture
3. Paste in Paint
4. Save as PNG

Mac:
1. Press Cmd+Shift+4
2. Drag to select area
3. File saves as PNG on desktop
```

#### Method C: Browser Extension
- Install "Full Page Screen Capture" or similar
- Works on all browsers
- Captures full quality

---

## FAQ

**Q: Why PNG instead of PDF?**
A: PNG is better for:
- Inserting in documents
- Web use
- Image editing software
- Consistent colors
- Smaller file size

**Q: Can I export as PDF?**
A: Yes! Press `Ctrl+P` and select "Save as PDF"

**Q: What resolution is the PNG?**
A: Matches your screen resolution (typically 1920x1080 or higher)

**Q: Can I export higher resolution?**
A: Yes! Zoom in browser (Ctrl++) before exporting

**Q: Why is filename so long?**
A: Includes metric and year for easy organization. You can rename after download.

**Q: Can I export multiple maps at once?**
A: No, but you can:
1. Export one
2. Change year/metric
3. Export again
4. Repeat

---

## Example Workflow

### Creating a Report with Multiple Maps:

```
1. Select "Actual Yield" + "2019" → Press E
2. Select "Actual Yield" + "2020" → Press E  
3. Select "Actual Yield" + "2021" → Press E
4. Select "Actual Yield" + "Average" → Press E
5. Select "Yield Gap" + "Average" → Press E

Result: 5 PNG files ready for your report!
```

---

## Browser Compatibility

| Browser | PNG Export | Color Legend | Crop to Bounds |
|---------|------------|--------------|----------------|
| Chrome 120+ | ✅ Perfect | ✅ Yes | ✅ Yes |
| Firefox 120+ | ✅ Perfect | ✅ Yes | ✅ Yes |
| Edge 120+ | ✅ Perfect | ✅ Yes | ✅ Yes |
| Safari 17+ | ⚠️ Good | ✅ Yes | ✅ Yes |
| Opera | ✅ Perfect | ✅ Yes | ✅ Yes |

✅ = Works perfectly
⚠️ = Works but may need manual rename

---

## Known Limitations

1. **Resolution**: Limited to screen resolution (can zoom for higher)
2. **Vector**: PNG is raster (not vector like PDF)
3. **Interactive**: Exported image is static (not interactive)
4. **Tiles**: Requires internet for base map tiles
5. **Size**: File size depends on map detail (~500KB-2MB typical)

---

## Support

If PNG export is not working:

1. ✅ Check browser console (F12) for errors
2. ✅ Try different browser (Chrome recommended)
3. ✅ Ensure internet connection (loads libraries)
4. ✅ Try refreshing page
5. ✅ Use fallback method (Ctrl+P or screenshot)

---

**Version**: 2.1  
**Last Updated**: December 2025  
**Status**: ✅ Working

Happy exporting! 📸🗺️


