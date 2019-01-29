let MAP_CENTER = new L.latLng(18.579916, -72.294903); // Port-au-Prince airport
let gisMap = 'undefined'

// Callback from django-leaflet on map initialization
function waterGISInit(map, options) {
    gisMap = map
    // Set map center to haiti
    map.setView(MAP_CENTER, 8);

    var osmUrl = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
            osm = L.tileLayer(osmUrl, { maxZoom: 18, attribution: '' }),
            drawnItems = L.featureGroup().addTo(map);

    // Enable drawing
    L.control.layers({
        'OSM': osm.addTo(map),
        "Google": L.tileLayer('http://www.google.cn/maps/vt?lyrs=s@189&gl=cn&x={x}&y={y}&z={z}', {
            attribution: 'Google'
        })
    }, { 'drawlayer': drawnItems }, { position: 'topleft', collapsed: false }).addTo(map);
    map.addControl(new L.Control.Draw({
        edit: {
            featureGroup: drawnItems,
            poly: {
                allowIntersection: false
            }
        },
        draw: {
            polygon: {
                allowIntersection: false,
                showArea: true
            }
        }
    }));
    map.addControl(new drawerControl());

    map.on(L.Draw.Event.CREATED, function (event) {
        var layer = event.layer;
        console.log(layer.toGeoJSON());
        drawnItems.addLayer(layer);
    });

    // Hide toolbar as we trigger draw per table item
    $(".leaflet-draw-toolbar").attr('hidden', true)
}

var drawerControl = L.Control.extend({
    options: {
        position: 'topright'
        //control position - allowed: 'topleft', 'topright', 'bottomleft', 'bottomright'
    },

    onAdd: function (map) {
        var container = L.DomUtil.create('i', 'leaflet-bar leaflet-control leaflet-drawer-control fas fa-arrow-left');
        container.style.backgroundColor = 'white';
        container.style.width = '25px';
        container.style.height = '25px';
        container.onclick = function(){
            toggleDrawer();
        }
        return container;
    }

});

function drawTest(){
    console.log("starting");
    let map = getMap();

    let polygon = new L.Draw.Polygon(map);
    polygon.enable();
}

function getMap(){
    return gisMap;
}

// Toggle the "details" drawer
function toggleDrawer(){
    let mapContainer = $('#map-container');
    let controlContainer = $('.leaflet-drawer-control')

    if (mapContainer.hasClass('col-md-9')){
        mapContainer.removeClass('col-md-9');
        mapContainer.addClass('col-md-12');
        controlContainer.removeClass('fa-arrow-right');
        controlContainer.addClass('fa-arrow-left');
    }
    else {
        mapContainer.addClass('col-md-9');
        mapContainer.removeClass('col-md-12');
        controlContainer.addClass('fa-arrow-right');
        controlContainer.removeClass('fa-arrow-left');
    }
    $('#details').collapse('toggle');
}
