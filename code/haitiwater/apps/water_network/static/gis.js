let MAP_CENTER = new L.latLng(18.579916, -72.294903); // Port-au-Prince airport
let gisMap = 'undefined'

function waterGISInit(map, options) {
    gisMap = map
    // Set map center to haiti
    map.setView(MAP_CENTER, 8);

    var osmUrl = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
            osmAttrib = '&copy; <a href="http://openstreetmap.org/copyright">OpenStreetMap</a> contributors',
            osm = L.tileLayer(osmUrl, { maxZoom: 18, attribution: osmAttrib }),
            drawnItems = L.featureGroup().addTo(map);

    // Enable drawing
    L.control.layers({
        'OSM': osm.addTo(map),
        "Google": L.tileLayer('http://www.google.cn/maps/vt?lyrs=s@189&gl=cn&x={x}&y={y}&z={z}', {
            attribution: 'google'
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

    map.on(L.Draw.Event.CREATED, function (event) {
        var layer = event.layer;
        console.log(layer.toGeoJSON());
        drawnItems.addLayer(layer);
    });

    // Hide toolbar as we trigger draw per table item
    $(".leaflet-draw-toolbar").attr('hidden', true)
}

function drawTest(){
    console.log("starting");
    let map = getMap();

    let polygon = new L.Draw.Polygon(map);
    polygon.enable();
}

function getMap(){
    return gisMap;
}
