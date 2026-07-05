document.addEventListener('DOMContentLoaded', () => {
    const mapEl = document.getElementById('map');
    if (!mapEl || typeof L === 'undefined') return;

    // Default center
    const map = L.map('map').setView([39.8283, -98.5795], 4);

    // Add OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    if (window.mapLocations && window.mapLocations.length > 0) {
        const bounds = L.latLngBounds();
        
        window.mapLocations.forEach(loc => {
            const marker = L.marker([loc.lat, loc.lng]).addTo(map);
            marker.bindPopup(`<a href="${loc.url}" style="font-weight: bold;">${loc.title}</a>`);
            bounds.extend([loc.lat, loc.lng]);
        });
        
        // Fit map to markers
        if (window.mapLocations.length > 0) {
            map.fitBounds(bounds, { padding: [50, 50], maxZoom: 15 });
        }
    }
});
