let MAP_CENTER = new L.latLng(18.579916, -72.294903); // Port-au-Prince airport

let gisMap = 'undefined';
let waterElementTable = 'undefined';
let detailTable = 'undefined';
let errorDetailTable = 'undefined';

let currentElementType = 'undefined';
let currentElementAddress = 'undefined';
let currentElementID = 'undefined';

let pointLayer = 'undefined';

$(document).ready(function() {
    drawWaterElementTable(false, true);
    waterElementTable = $("#datatable-water_element").DataTable()
    detailTable = $("#detail-table");
    errorDetailTable = $('#error-detail-table')

    $('#datatable-water_element tbody').on( 'click', 'tr', function () {
        let data = waterElementTable.row(this).data();
        setupWaterElementDetails(data[0]);
    });

    waterGISInit(
        L.map('map-water-network',
        {
            zoomControl: false //Set as fale to instantiate custom zoom control
        })
    );

    waterGISPopulate();
});

function waterGISPopulate(){
    let elementPosition = requestElementPosition();
    if( !elementPosition ){
        // Request failed
        return; //Maybe hide map, or use cached data, update as needed
    }
    //Todo populate map from DB
}

function requestElementPosition(){
    let requestURL = "../api/gis?marker=all";
    let xhttp = new XMLHttpRequest();

    xhttp.onreadystatechange = function(){
        if (this.readyState == 4 && this.status == 200) {
            return JSON.parse(this.responseText);
        }
        else if (this.readyState == 4){
            console.log(this);
            new PNotify({
                title: 'Erreur',
                text: 'Les positions ne peuvent être téléchargées',
                type: 'error'
            });
            return false;
        }
    }
    xhttp.open('GET', requestURL, true);
    xhttp.send();
}

function waterGISInit(map) {
    gisMap = map
    // Set map center to haiti
    map.setView(MAP_CENTER, 8);

    var osmUrl = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        osm = L.tileLayer(osmUrl, { maxZoom: 18, attribution: '' }),
        waterElement = L.featureGroup().addTo(map);

    pointLayer = waterElement;
    L.control.zoom({
        position:'topleft',
        zoomInTitle:'Agrandir',
        zoomOutTitle:'Réduire',
    }).addTo(map);
    // Enable drawing
    L.control.layers({
        'OSM': osm.addTo(map),
        "Google": L.tileLayer('http://www.google.cn/maps/vt?lyrs=s@189&gl=cn&x={x}&y={y}&z={z}', {
            attribution: 'Google'
        })
    }, { "Réseau": waterElement }, { position: 'topleft', collapsed: false }).addTo(map);
    map.addControl(new L.Control.Draw({
        edit: {
            featureGroup: waterElement,
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

function setupWaterElementDetails(elementID){
    let response = requestWaterElementDetails(elementID);
    if (!response){
        detailTable.addClass('hidden');
        errorDetailTable.removeClass('hidden');
        readyMapDrawButtons('pipe', false) // Fake, used for testing
        return;
    }
    detailTable.removeClass('hidden');
    errorDetailTable.addClass('hidden');

    console.log('Successfuly retrieved JSON: ' + response);

    $("#element-details-id").html(response.id);
    $("#element-details-type").html(response.type);
    $("#element-details-localization").html(response.localization);
    $("#element-details-manager").html(response.manager);
    $("#element-details-users").html(response.users);
    $("#element-details-state").html(response.state);
    $("#element-details-current-month-cubic").html(response.currentMonthCubic);
    $("#element-details-average-month-cubic").html(response.averageMonthCubic);
    $("#element-details-total-cubic").html(response.totalCubic);

    currentElementID = response.id;
    currentElementType = response.type;
    currentElementAddress = response.localization;

    readyMapDrawButtons(response.type, response.localization);
}

function readyMapDrawButtons(type, hasPosition){
    console.log('prepping buttons');
    let drawButton = $('#button-draw');
    let editButton = $('#button-edit');
    let removebutton = $('#button-remove');

    //You can only create non-existing positions, or edit/delete existing ones
    drawButton.prop('disabled', hasPosition);
    editButton.prop('disabled', !hasPosition);
    removebutton.prop('disabled', !hasPosition);

    //Attach the handlers
    if(!hasPosition){
        console.log("attaching draw event");
        //Creating a position
        drawButton.on('click', {type:type}, drawHandler);
    }
}

function drawHandler( e ){
    let type = e.data.type;
    let map = getMap();
    let isPoint = (type == 'fountain' || type == 'kiosk' || type == 'individual');
    let isPolyline = (type == 'pipe');
    if( isPoint ){
        let pointDrawer = new L.Draw.Marker(map);
        pointDrawer.enable();
        map.on(L.Draw.Event.CREATED,saveDraw);
    }
    else if ( isPolyline ){
        let polyLineDrawer = new L.Draw.Polyline(map);
        polyLineDrawer.enable();
        map.on(L.Draw.Event.CREATED, saveDraw);
    }
    else {
        console.log("Implement further options if required");
        // A polygon for zones would be a good example
    }
}

function saveDraw(event){
    let map = getMap();
    var layer = event.layer;
    layer.bindTooltip('my tooltip', {
        sticky:true
    });
    console.log(layer.toGeoJSON());
    pointLayer.addLayer(layer);

    sendDrawToServer(layer.toGeoJSON());

    //Destroy handlers
    map.off(L.Draw.Event.CREATED, saveDraw);
    let drawButton = $('#button-draw');
    drawButton.off('click', drawHandler)
}

function sendDrawToServer(geoJSON){
    let coordinates = JSON.stringify(geoJSON.geometry.coordinates);
    let requestURL = "../api/gis?id=" + currentElementID + "&coordinates=" + coordinates;
    console.log('save request : ' +requestURL);
    let xhttp = new XMLHttpRequest();

    xhttp.onreadystatechange = function(){
        if (this.readyState == 4 && this.status == 200) {
            return JSON.parse(this.responseText);
        }
        else if (this.readyState == 4){
            console.log(this);
            let msg = "Une erreur est survenue:<br>"+ this.status + ": " + this.statusText
            errorDetailTable.html(msg);
            return this;
        }
    }

    xhttp.open('POST', requestURL, true);
    xhttp.send();
}

function requestWaterElementDetails(elementID){
    let requestURL = "../api/details?table=water_element&id="+elementID;
    let xhttp = new XMLHttpRequest();

    xhttp.onreadystatechange = function(){
        if (this.readyState == 4 && this.status == 200) {
            return JSON.parse(this.responseText);
        }
        else if (this.readyState == 4){
            console.log(this);
            let msg = "Une erreur est survenue:<br>"+ this.status + ": " + this.statusText
            errorDetailTable.html(msg);
            return this;
        }
    }

    xhttp.open('GET', requestURL, true);
    xhttp.send();

}
