let MAP_CENTER = new L.latLng(18.579916, -72.294903); // Port-au-Prince airport

// Frequently accessed page elements
let gisMap = 'undefined';
let waterElementTable = 'undefined';
let detailTable = 'undefined';
let errorDetailTable = 'undefined';
let drawLayer = 'undefined';

// Current element selection shared variables
let currentElementType = 'undefined';
let currentElementAddress = 'undefined';
let currentElementID = 'undefined';


$(document).ready(function() {
    //Setup water tables first
    drawWaterElementTable(false, true);
    waterElementTable = $("#datatable-water_element").DataTable()
    detailTable = $("#detail-table");
    errorDetailTable = $('#error-detail-table')

    //Request details on element click
    $('#datatable-water_element tbody').on( 'click', 'tr', function () {
        let data = waterElementTable.row(this).data();
        requestWaterElementDetails(data[0]);
    });

    //Init Leaflet map
    waterGISInit(
        L.map('map-water-network',
        {
            zoomControl: false //Set as fale to instantiate custom zoom control
        })
    );

    //Populate map with known elements
    requestAllElementsPosition();
});

/**
 * Populates the Leaflet map with the positions from the server
 */
function waterGISPopulate(elementPosition){
    if( !elementPosition ){
        // Request failed
        return; //Maybe hide map, or use cached data, update as needed
    }
    for(let id in elementPosition){
        let tooltip = elementPosition[id][0];
        let geoJSON = jQuery.parseJSON(elementPosition[id][1]);

        let drawElement = L.geoJSON(geoJSON).addTo(drawLayer);
        drawElement.on('click', function(e){
            $('.selected').removeClass('selected');
            requestWaterElementDetails(id);
        });
    }
    //Todo populate map from DB
    // 1. Get array
    // 2. Draw elements on map
    // 3. Set tooltip on hover
    // 4. Set link on click
}


/**
 * Request all known element positions from the server
 * @return {[JSONArray]} [The positions as a list of GeoJSON]
 */
function requestAllElementsPosition(){
    let requestURL = "../api/gis?marker=all";
    let xhttp = new XMLHttpRequest();

    xhttp.onreadystatechange = function(){
        if (this.readyState == 4 && this.status == 200) {
            waterGISPopulate(JSON.parse(this.response));
        }
        else if (this.readyState == 4){
            console.log(this);
            new PNotify({
                title: 'Erreur',
                text: 'Les positions ne peuvent être téléchargées',
                type: 'error'
            });
            waterGISPopulate(false);
        }
    }
    xhttp.open('GET', requestURL, true);
    xhttp.send();
}

/**
 * Initialize the water element GIS map
 * @param  {[L.map]} map [An instantiated leaflet map]
 */
function waterGISInit(map) {
    gisMap = map;
    // Set map center to haiti
    map.setView(MAP_CENTER, 8);

    // Custom zoom control to allow french language
    L.control.zoom({
        position:'topleft',
        zoomInTitle:'Agrandir',
        zoomOutTitle:'Réduire',
    }).addTo(map);

    // Open Street maps layer
    let osmUrl = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
    let osm = L.tileLayer(osmUrl, {maxZoom: 18, attribution: 'Open Street Maps' });

    // Google sattelite layer
    let googleUrl = 'http://www.google.cn/maps/vt?lyrs=s@189&gl=cn&x={x}&y={y}&z={z}';
    let google = L.tileLayer(googleUrl, {attribution: 'Google'});

    // Draw layer
    let waterElement = L.featureGroup().addTo(map);
    drawLayer = waterElement;

    // Setup layers
    L.control.layers(
        { // Base layers
            'Carte': osm.addTo(map), // default layer
            'Sattelite': google
        },
        { // Overlays
            'Réseau': waterElement
        },
        { // Options
            position: 'topleft',
            collapsed: false
        }).addTo(map);

    // Control to collapse details panel
    map.addControl(new drawerControl());
}

/**
 * The drawer control is displayed on the map to expand/retract the details panel
 * @type {L.Control}
 */
var drawerControl = L.Control.extend({
    options: {
        position: 'topright'
    },

    onAdd: function (map) {
        var container = L.DomUtil.create('i', 'leaflet-bar leaflet-control leaflet-drawer-control fas fa-arrow-left');
        container.style.backgroundColor = 'white';
        container.style.width = '25px';
        container.style.height = '25px';
        container.onclick = function(){
            toggleDrawer();
        };
        return container;
    }

});

/**
 * Toggle the detail drawer
 */
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

/**
 * Requests the details of an element to the server
 * @param  {int} elementID
 */
function requestWaterElementDetails(elementID){
    let requestURL = "../api/details?table=water_element&id="+elementID;
    let xhttp = new XMLHttpRequest();

    xhttp.onreadystatechange = function(){
        if (this.readyState == 4 && this.status == 200) {
            setupWaterElementDetails(JSON.parse(this.response));
        }
        else if (this.readyState == 4){
            console.log(this);
            let msg = "Une erreur est survenue:<br>"+ this.status + ": " + this.statusText;
            errorDetailTable.html(msg);
            return setupWaterElementDetails(false);
        }
    };

    xhttp.open('GET', requestURL, true);
    xhttp.send();

}

/**
 * Setup the display for the selected element details
 * @param  {JSON} response The element details
 */
function setupWaterElementDetails(response){
    if (!response){
        detailTable.addClass('hidden');
        errorDetailTable.removeClass('hidden');
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

    let hasLocalization = response.geoJSON !== null;
    readyMapDrawButtons(response.type, hasLocalization);
}

/**
 * Display the buttons accordingly
 * @param  {string}  type        type of the water element
 * @param  {Boolean} hasPosition true if the element already is on the map
 */
function readyMapDrawButtons(type, hasPosition){
    resetMapDrawButtons();
    let drawButton = $('#button-draw');
    let editButton = $('#button-edit');
    let removeButton = $('#button-remove');

    //You can only create non-existing positions, or edit/delete existing ones
    drawButton.prop('disabled', hasPosition);
    editButton.prop('disabled', hasPosition);
    removeButton.prop('disabled', !hasPosition);

    //Attach the handlers
    if(!hasPosition){
        drawButton.on('click', {type:type}, drawHandler);
        editButton.on('click', {type:type}, editHandler);
    } else {
        removeButton.on('click', removeHandler)
    }
}

function resetMapDrawButtons(){
    let map = gisMap;
    let drawButton = $('#button-draw');
    let editButton = $('#button-edit');
    let removeButton = $('#button-remove');

    map.off(L.Draw.Event.CREATED, saveDraw);
    drawButton.off();
    editButton.off();
    removeButton.off();
}

/**
 * Handles a click on the draw button
 * @param  {Event} e the click event
 */
function drawHandler( e ){
    let type = e.data.type.toLowerCase();
    let map = gisMap;
    let isPoint = (type == 'fontaine' || type == 'kiosque' || type == 'prise individuelle' );
    let isPolyline = (type == 'conduite');
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

/**
 * Save a draw on the layer and send it to server
 * @param  {L.Draw.CREATED} event
 */
function saveDraw(event){
    // Save it on the map
    let map = gisMap;
    var layer = event.layer;
    layer.bindTooltip('my tooltip', { // Todo change for format tooltip
        sticky:true
    });
    layer.waterID = 'customID';
    layer.on('click', function(e){
        console.log(this); // Todo link to details request and table focus
    });
    drawLayer.addLayer(layer);

    // Save it on the server
    sendDrawToServer(layer.toGeoJSON());
}

/**
 * Save a position on the server
 * @param  {GeoJSON} geoJSON of the object to save
 */
function sendDrawToServer(geoJSON){
    let requestURL = "../api/gis/?action=add&id=" + currentElementID;
    let xhttp = new XMLHttpRequest();

    xhttp.onreadystatechange = function(){
        if (this.readyState == 4 && this.status == 200) {
            console.log(this);
        }
        else if (this.readyState == 4){
            console.log(this);
            let msg = "Une erreur est survenue:<br>"+ this.status + ": " + this.statusText;
            errorDetailTable.html(msg);
            return this;
        }
    }

    xhttp.open('POST', requestURL, true);
    xhttp.setRequestHeader('Content-Type', 'application/json');
    xhttp.send(JSON.stringify(geoJSON));
}

function removeHandler(e){
    let requestURL = "../api/gis/?action=remove&id=" + currentElementID;
    let xhttp = new XMLHttpRequest();

    xhttp.onreadystatechange = function(){
        if (this.readyState == 4 && this.status == 200) {
            readyMapDrawButtons(currentElementType, false);
        }
        else if (this.readyState == 4){
            console.log(this);
            new PNotify({
                title: 'Erreur',
                text: "L'élément ne peut être supprimé: " + this.statusText,
                type: 'error'
            });
            return this;
        }
    };

    xhttp.open('POST', requestURL, true);
    xhttp.send();
}