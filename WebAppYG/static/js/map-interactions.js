// Enhanced map interactions for Morocco Yield Gap Analysis Platform

// Global variables for map interactions
let selectedRegion = null;
let regionStatistics = {};
let zoomLevel = 6;

// Initialize map interactions
function initializeMapInteractions() {
    // Add custom controls
    addCustomControls();
    
    // Add keyboard shortcuts
    addKeyboardShortcuts();
    
    // Add touch gestures for mobile
    addTouchGestures();
    
    // Add export functionality
    addExportFeatures();
}

// Add custom map controls
function addCustomControls() {
    // Zoom to Morocco control
    const zoomToMoroccoControl = L.control({position: 'topleft'});
    zoomToMoroccoControl.onAdd = function(map) {
        const div = L.DomUtil.create('div', 'custom-control');
        div.innerHTML = '<button class="btn" onclick="zoomToMorocco()" title="Zoom to Morocco"><i class="fas fa-home"></i></button>';
        return div;
    };
    zoomToMoroccoControl.addTo(map);
    
    // Fullscreen control
    const fullscreenControl = L.control({position: 'topleft'});
    fullscreenControl.onAdd = function(map) {
        const div = L.DomUtil.create('div', 'custom-control');
        div.innerHTML = '<button class="btn" onclick="toggleFullscreen()" title="Toggle Fullscreen"><i class="fas fa-expand"></i></button>';
        return div;
    };
    fullscreenControl.addTo(map);
    
    // Layer opacity control
    const opacityControl = L.control({position: 'topright'});
    opacityControl.onAdd = function(map) {
        const div = L.DomUtil.create('div', 'opacity-control');
        div.innerHTML = `
            <label>Layer Opacity:</label>
            <input type="range" id="opacity-slider" min="0" max="1" step="0.1" value="0.7" onchange="updateLayerOpacity(this.value)">
        `;
        return div;
    };
    opacityControl.addTo(map);
}

// Zoom to Morocco bounds
function zoomToMorocco() {
    const moroccoBounds = L.latLngBounds(
        L.latLng(27.0, -17.0), // Southwest corner
        L.latLng(36.0, -1.0)   // Northeast corner
    );
    map.fitBounds(moroccoBounds);
}

// Toggle fullscreen mode
function toggleFullscreen() {
    if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen();
    } else {
        document.exitFullscreen();
    }
}

// Update layer opacity
function updateLayerOpacity(opacity) {
    currentLayers.forEach(layer => {
        layer.setStyle({fillOpacity: opacity});
    });
}

// Add keyboard shortcuts
function addKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        switch(e.key) {
            case 'Escape':
                document.getElementById('region-info-panel').style.display = 'none';
                break;
            case 'r':
            case 'R':
                if (e.ctrlKey) {
                    e.preventDefault();
                    updateMap();
                }
                break;
            case 'e':
            case 'E':
                if (e.ctrlKey) {
                    e.preventDefault();
                    exportData();
                }
                break;
            case 'f':
            case 'F':
                if (e.ctrlKey) {
                    e.preventDefault();
                    toggleFullscreen();
                }
                break;
        }
    });
}

// Add touch gestures for mobile
function addTouchGestures() {
    let touchStartX = 0;
    let touchStartY = 0;
    
    map.getContainer().addEventListener('touchstart', function(e) {
        touchStartX = e.touches[0].clientX;
        touchStartY = e.touches[0].clientY;
    });
    
    map.getContainer().addEventListener('touchend', function(e) {
        const touchEndX = e.changedTouches[0].clientX;
        const touchEndY = e.changedTouches[0].clientY;
        const deltaX = touchEndX - touchStartX;
        const deltaY = touchEndY - touchStartY;
        
        // Swipe left to close info panel
        if (deltaX < -50 && Math.abs(deltaY) < 50) {
            document.getElementById('region-info-panel').style.display = 'none';
        }
    });
}

// Enhanced region click handler
function handleRegionClick(e, data) {
    selectedRegion = data;
    
    // Update statistics
    updateRegionStatistics(data);
    
    // Show detailed info
    showRegionInfo(data);
    
    // Highlight selected region
    highlightSelectedRegion(data);
    
    // Update chart
    updateRegionChart(data);
    
    // Log interaction
    logUserInteraction('region_click', data.boundary_name);
}

// Update region statistics
function updateRegionStatistics(data) {
    regionStatistics = {
        name: data.boundary_name,
        crop: data.crop_name,
        year: data.year,
        actualYield: data.actual_yield,
        potentialYield: data.potential_yield,
        yieldGap: data.yield_gap,
        yieldGapPercent: data.yield_gap_percent,
        timestamp: new Date().toISOString()
    };
}

// Highlight selected region
function highlightSelectedRegion(data) {
    // Remove previous highlights
    currentLayers.forEach(layer => {
        layer.setStyle({
            weight: 2,
            opacity: 1,
            color: 'white',
            dashArray: '3'
        });
    });
    
    // Find and highlight selected region
    currentLayers.forEach(layer => {
        if (layer.feature && layer.feature.properties.name === data.boundary_name) {
            layer.setStyle({
                weight: 4,
                opacity: 1,
                color: '#ff6b6b',
                dashArray: '5, 5'
            });
        }
    });
}

// Update region-specific chart
function updateRegionChart(data) {
    if (!yieldChart) return;
    
    // Filter data for this region
    const regionData = yieldData.filter(d => d.boundary_name === data.boundary_name);
    
    const years = regionData.map(d => d.year);
    const actualYields = regionData.map(d => d.actual_yield);
    const potentialYields = regionData.map(d => d.potential_yield);
    
    yieldChart.data.labels = years;
    yieldChart.data.datasets = [
        {
            label: 'Actual Yield',
            data: actualYields,
            backgroundColor: 'rgba(102, 126, 234, 0.8)',
            borderColor: 'rgba(102, 126, 234, 1)',
            borderWidth: 1
        },
        {
            label: 'Potential Yield',
            data: potentialYields,
            backgroundColor: 'rgba(118, 75, 162, 0.8)',
            borderColor: 'rgba(118, 75, 162, 1)',
            borderWidth: 1
        }
    ];
    yieldChart.update();
}

// Add export features
function addExportFeatures() {
    // Export current view as image
    window.exportMapImage = function() {
        const mapContainer = document.getElementById('map');
        html2canvas(mapContainer).then(canvas => {
            const link = document.createElement('a');
            link.download = 'morocco-yield-map.png';
            link.href = canvas.toDataURL();
            link.click();
        });
    };
    
    // Export region data as JSON
    window.exportRegionData = function() {
        if (!selectedRegion) {
            alert('Please select a region first');
            return;
        }
        
        const dataStr = JSON.stringify(regionStatistics, null, 2);
        const dataBlob = new Blob([dataStr], {type: 'application/json'});
        const url = URL.createObjectURL(dataBlob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `${selectedRegion.boundary_name}-data.json`;
        link.click();
        URL.revokeObjectURL(url);
    };
}

// Log user interactions for analytics
function logUserInteraction(action, details) {
    const interaction = {
        action: action,
        details: details,
        timestamp: new Date().toISOString(),
        userAgent: navigator.userAgent,
        screenResolution: `${screen.width}x${screen.height}`,
        mapZoom: map.getZoom(),
        mapCenter: map.getCenter()
    };
    
    // Send to analytics endpoint (if available)
    fetch('/api/analytics/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(interaction)
    }).catch(error => console.log('Analytics not available:', error));
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeMapInteractions();
});

// Export functions for global access
window.zoomToMorocco = zoomToMorocco;
window.toggleFullscreen = toggleFullscreen;
window.updateLayerOpacity = updateLayerOpacity;
window.handleRegionClick = handleRegionClick;




