# 🧪 Test PNG Export Feature

## Quick Test Checklist

After starting the server, follow these steps to verify PNG export works:

### ✅ Step 1: Start Application
```bash
cd WebAppYG
conda activate WebAppYG
python manage.py runserver
```

### ✅ Step 2: Open Browser
- Go to: `http://127.0.0.1:8000/`
- Wait for map to fully load

### ✅ Step 3: Test Export Button
1. Select **Year**: Average
2. Select **Metric**: Actual Yield
3. Click **"Export Map (PNG)"** button
4. Wait for green notification: "Map exported successfully!"

### ✅ Step 4: Verify Download
Check your Downloads folder for file:
- **Name**: `Morocco_YieldGap_Actual_Yield_Average.png`
- **Type**: PNG image file (not PDF!)
- **Size**: ~500KB - 2MB

### ✅ Step 5: Open PNG File
1. Open the downloaded PNG
2. Verify you see:
   - ✅ Map of Morocco (cropped, no empty space)
   - ✅ Colored legend on the right side (NOT white!)
   - ✅ Title at top
   - ✅ Clear province boundaries
   - ✅ No sidebars or UI elements

### ✅ Step 6: Test Keyboard Shortcut
1. Back in browser
2. Select different metric (e.g., "Yield Gap")
3. Press **E** key
4. Verify PNG downloads

### ✅ Step 7: Test Different Years
1. Select **Year**: 2019
2. Press **E**
3. Verify PNG filename includes "2019"

---

## Expected Results

### ✅ Good Export Looks Like:

```
┌─────────────────────────────────────────────────────┐
│   Morocco Wheat Yield Gap Analysis                 │
│   Actual Yield - Average                            │
├─────────────────────────────────┬───────────────────┤
│                                 │  Legend           │
│         [Morocco Map]           │  ████ 8.0         │
│         [with colors]           │  ████ 7.0         │
│         [no empty space]        │  ████ 6.0         │
│                                 │  ████ 5.0         │
│                                 │  ████ 4.0         │
│                                 │  ████ 3.0         │
│                                 │  ████ 2.0         │
│                                 │  ████ 1.0         │
│                                 │  (t/ha)           │
└─────────────────────────────────┴───────────────────┘
Source: Morocco Yield Gap Analysis 2025
```

### ❌ Issues to Check:

**If legend is white/blank:**
- Wait 3 seconds after selecting metric before export
- Refresh page and try again
- Check browser console (F12) for errors

**If file is PDF:**
- Check file extension - might just be mislabeled
- Right-click file > Properties to verify type
- Try renaming .pdf to .png

**If map shows too much empty space:**
- Should auto-crop to Morocco
- Check if Morocco provinces are visible
- Try zooming in slightly before export

**If colors don't match screen:**
- This is now fixed - colors should match exactly
- If still wrong, report as bug

---

## Troubleshooting Tests

### Test 1: Check Libraries Loaded
1. Open browser console (F12)
2. Go to "Console" tab
3. Look for errors about "leaflet-image" or "html2canvas"
4. If errors, check internet connection

### Test 2: Verify Legend Colors
1. Select "Actual Yield" metric
2. Look at legend on map (lower left)
3. Colors should be green shades
4. Select "Yield Gap" metric
5. Colors should change to red shades
6. If legend is always white, there's a CSS issue

### Test 3: Check Download Location
```
Windows Default: C:\Users\[YourName]\Downloads\
```
- Search for "Morocco_YieldGap" in Downloads folder
- Sort by date to find most recent

### Test 4: Verify PNG Format
1. Right-click downloaded file
2. Select "Properties" (Windows) or "Get Info" (Mac)
3. Type should be: "PNG Image"
4. If not, try opening in image editor

---

## Browser-Specific Tests

### Chrome:
1. Should work perfectly
2. PNG downloads to default Downloads folder
3. No prompts needed

### Firefox:
1. Should work perfectly
2. May ask where to save
3. Ensure "Save File" is selected (not "Open with")

### Edge:
1. Should work perfectly
2. May show notification bar at top
3. Click "Open folder" to find file

---

## Success Criteria

**All of these should be TRUE:**

- [ ] File extension is `.png` (not .pdf or .webp)
- [ ] File opens as image
- [ ] Legend shows colored boxes (not white)
- [ ] Map is cropped to Morocco only
- [ ] Title shows correct metric and year
- [ ] File size is reasonable (500KB-2MB)
- [ ] Can open in Paint/Preview/GIMP
- [ ] Colors match what you see on screen
- [ ] Keyboard shortcut (E) works
- [ ] Multiple exports create separate files

---

## Fallback Options

If PNG export still doesn't work after fixes:

### Option A: Use Snipping Tool
**Windows 10/11:**
1. Press `Windows + Shift + S`
2. Select area to capture
3. Paste in Paint
4. Save as PNG

**Windows 7:**
1. Open "Snipping Tool"
2. New > Rectangular
3. Select area
4. Save as PNG

### Option B: Browser Extension
Install one of these (all free):
- "Nimbus Screenshot"
- "Awesome Screenshot"
- "Full Page Screen Capture"

### Option C: Print to PDF then Convert
1. Press `Ctrl + P`
2. Save as PDF
3. Use online tool to convert PDF → PNG
   - pdf2png.com
   - cloudconvert.com
   - zamzar.com

---

## Report Results

After testing, report:

✅ **Working**: "PNG export works! Colors shown, Morocco cropped, file is .png"

❌ **Not Working**: Include:
- Browser name and version
- What happened (PDF? White legend? Wrong crop?)
- Any error messages
- Screenshot of downloaded file
- Screenshot of browser console (F12)

---

## Performance Notes

**Export Speed:**
- Small screen (1366x768): ~2 seconds
- Medium screen (1920x1080): ~3 seconds  
- Large screen (2560x1440): ~5 seconds
- 4K screen (3840x2160): ~8 seconds

**File Size:**
- Typical: 800KB - 1.5MB
- With many provinces: 1.5MB - 2.5MB
- Maximum expected: 3MB

---

**Status**: Ready to test! 🧪
**Version**: 2.1 (PNG Export Fixed)
**Date**: December 2025

Good luck with testing! 📸✅


