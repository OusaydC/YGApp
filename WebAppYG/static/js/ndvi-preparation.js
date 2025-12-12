// NDVI Preparation Module for Morocco Yield Gap Analysis Platform

// NDVI data structure
let ndviData = {};
let ndviLayers = {};
let currentNDVILayer = null;

// NDVI color scale (red to green)
const ndviColorScale = [
    '#8B0000', // Dark red (low vegetation)
    '#FF0000', // Red
    '#FFA500', // Orange
    '#FFFF00', // Yellow
    '#ADFF2F', // Green yellow
    '#00FF00', // Green
    '#008000', // Dark green (high vegetation)
    '#006400'  // Forest green
];

// Initialize NDVI functionality
function initializeNDVI() {
    // Add NDVI controls to the UI
    addNDVIControls();
    
    // Load sample NDVI data
    loadSampleNDVIData();
    
    // Set up NDVI layer switching
    setupNDVILayerSwitching();
}

// Add NDVI controls to the sidebar
function addNDVIControls() {
    const sidebar = document.querySelector('.sidebar');
    
    // Create NDVI control group
    const ndviControlGroup = document.createElement('div');
    ndviControlGroup.className = 'control-group';
    ndviControlGroup.innerHTML = `
        <label><i class="fas fa-leaf"></i> NDVI Analysis</label>
        <div class="ndvi-controls">
            <button class="btn btn-success" onclick="toggleNDVI()">
                <i class="fas fa-toggle-on"></i> Toggle NDVI
            </button>
            <select id="ndvi-date-select" onchange="updateNDVIDate()">
                <option value="2024-01-01">January 2024</option>
                <option value="2024-02-01">February 2024</option>
                <option value="2024-03-01">March 2024</option>
                <option value="2024-04-01">April 2024</option>
                <option value="2024-05-01">May 2024</option>
                <option value="2024-06-01">June 2024</option>
            </select>
            <div class="ndvi-legend">
                <h5>NDVI Scale</h5>
                <div class="ndvi-scale">
                    <span style="color: #8B0000;">Low</span>
                    <span style="color: #00FF00;">High</span>
                </div>
            </div>
        </div>
    `;
    
    // Insert after the last control group
    const lastControlGroup = sidebar.querySelector('.control-group:last-of-type');
    sidebar.insertBefore(ndviControlGroup, lastControlGroup);
}

// Load sample NDVI data (replace with real API call)
function loadSampleNDVIData() {
    // Sample NDVI data for demonstration
    ndviData = {
        '2024-01-01': generateSampleNDVIData(0.3, 0.7),
        '2024-02-01': generateSampleNDVIData(0.4, 0.8),
        '2024-03-01': generateSampleNDVIData(0.5, 0.9),
        '2024-04-01': generateSampleNDVIData(0.6, 0.95),
        '2024-05-01': generateSampleNDVIData(0.7, 0.98),
        '2024-06-01': generateSampleNDVIData(0.8, 0.99)
    };
}

// Generate sample NDVI data for regions
function generateSampleNDVIData(minNDVI, maxNDVI) {
    const regions = [
        'Casablanca-Settat', 'Rabat-Salé-Kénitra', 'Fès-Meknès',
        'Marrakech-Safi', 'Tanger-Tétouan-Al Hoceïma', 'Oriental',
        'Béni Mellal-Khénifra', 'Souss-Massa', 'Drâa-Tafilalet',
        'Guelmim-Oued Noun', 'Laâyoune-Sakia El Hamra', 'Dakhla-Oued Ed-Dahab'
    ];
    
    const ndviData = {};
    regions.forEach(region => {
        // Generate random NDVI values between min and max
        const ndvi = Math.random() * (maxNDVI - minNDVI) + minNDVI;
        ndviData[region] = {
            value: ndvi,
            status: getNDVIStatus(ndvi),
            color: getNDVIColor(ndvi)
        };
    });
    
    return ndviData;
}

// Get NDVI status based on value
function getNDVIStatus(ndvi) {
    if (ndvi < 0.2) return 'Bare soil/Water';
    if (ndvi < 0.4) return 'Sparse vegetation';
    if (ndvi < 0.6) return 'Moderate vegetation';
    if (ndvi < 0.8) return 'Dense vegetation';
    return 'Very dense vegetation';
}

// Get NDVI color based on value
function getNDVIColor(ndvi) {
    const index = Math.floor(ndvi * (ndviColorScale.length - 1));
    return ndviColorScale[index];
}

// Toggle NDVI layer
function toggleNDVI() {
    const button = document.querySelector('.ndvi-controls button');
    const isActive = button.classList.contains('active');
    
    if (isActive) {
        // Hide NDVI layer
        hideNDVILayer();
        button.classList.remove('active');
        button.innerHTML = '<i class="fas fa-toggle-off"></i> Toggle NDVI';
    } else {
        // Show NDVI layer
        showNDVILayer();
        button.classList.add('active');
        button.innerHTML = '<i class="fas fa-toggle-on"></i> Hide NDVI';
    }
}

// Show NDVI layer
function showNDVILayer() {
    const selectedDate = document.getElementById('ndvi-date-select').value;
    const ndviDataForDate = ndviData[selectedDate];
    
    if (!ndviDataForDate) return;
    
    // Create NDVI layer
    currentNDVILayer = L.layerGroup();
    
    // Add NDVI data to regions
    yieldData.forEach(data => {
        if (data.geometry && ndviDataForDate[data.boundary_name]) {
            try {
                const geoJson = JSON.parse(data.geometry);
                const ndviInfo = ndviDataForDate[data.boundary_name];
                
                const layer = L.geoJSON(geoJson, {
                    style: {
                        fillColor: ndviInfo.color,
                        weight: 2,
                        opacity: 1,
                        color: 'white',
                        fillOpacity: 0.7
                    }
                });
                
                layer.bindPopup(`
                    <div style="min-width: 200px;">
                        <h4 style="color: #2c3e50; margin-bottom: 10px;">${data.boundary_name}</h4>
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px;">
                            <div><strong>NDVI Value:</strong> ${ndviInfo.value.toFixed(3)}</div>
                            <div><strong>Status:</strong> ${ndviInfo.status}</div>
                            <div><strong>Date:</strong> ${selectedDate}</div>
                            <div><strong>Crop:</strong> ${data.crop_name}</div>
                        </div>
                    </div>
                `);
                
                currentNDVILayer.addLayer(layer);
            } catch (e) {
                console.error('Error parsing NDVI geometry for', data.boundary_name, e);
            }
        }
    });
    
    currentNDVILayer.addTo(map);
}

// Hide NDVI layer
function hideNDVILayer() {
    if (currentNDVILayer) {
        map.removeLayer(currentNDVILayer);
        currentNDVILayer = null;
    }
}

// Update NDVI date
function updateNDVIDate() {
    if (currentNDVILayer) {
        hideNDVILayer();
        showNDVILayer();
    }
}

// Setup NDVI layer switching
function setupNDVILayerSwitching() {
    // Add keyboard shortcut for NDVI toggle
    document.addEventListener('keydown', function(e) {
        if (e.key === 'n' || e.key === 'N') {
            if (e.ctrlKey) {
                e.preventDefault();
                toggleNDVI();
            }
        }
    });
}

// Export NDVI data
function exportNDVIData() {
    const selectedDate = document.getElementById('ndvi-date-select').value;
    const ndviDataForDate = ndviData[selectedDate];
    
    if (!ndviDataForDate) {
        alert('No NDVI data available for the selected date');
        return;
    }
    
    const exportData = {
        date: selectedDate,
        regions: ndviDataForDate,
        metadata: {
            source: 'Sentinel-2',
            resolution: '10m',
            processing_date: new Date().toISOString()
        }
    };
    
    const dataStr = JSON.stringify(exportData, null, 2);
    const dataBlob = new Blob([dataStr], {type: 'application/json'});
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `ndvi-data-${selectedDate}.json`;
    link.click();
    URL.revokeObjectURL(url);
}

// Initialize NDVI when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize NDVI after a short delay to ensure other components are loaded
    setTimeout(initializeNDVI, 1000);
});

// Export functions for global access
window.toggleNDVI = toggleNDVI;
window.updateNDVIDate = updateNDVIDate;
window.exportNDVIData = exportNDVIData;




