$(document).ready(function() {
    // Draw the water element table with the managers
    drawWaterElementTable(true, true);
    // Draw the managers table
    drawManagersTable();
    // Draw the zone table
    drawZoneTable();

    $('#multiselect-outlets').select2({
        dropdownParent: $('#modalManager'),
        width: '100%',
    });
});
