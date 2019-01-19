$(document).ready(function() {
    // Draw the water element table with the managers
    drawWaterElementTable(true, true);
    // Draw the managers table
    drawManagerTable();
    // Draw the zone table
    drawZoneTable();

    $('#multiselect-manager-outlets').select2({
        dropdownParent: $('#modalManager'),
        width: '100%',
    });
});
