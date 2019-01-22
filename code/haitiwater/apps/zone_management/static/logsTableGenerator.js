$(document).ready(function() {
    // Draw the water element table without the managers
    drawLogTable();
});


function drawLogTable(){
    let baseURL = location.protocol+'//'+location.hostname+(location.port ? ':'+location.port: '');
    let dataURL = baseURL + "/api/table/?name=logs";
    console.log("Request data from: " + dataURL);
    $('#datatable-logs').DataTable(getLogsTableConfiguration(dataURL));
    let table = $('#datatable-logs').DataTable();

    $('#datatable-logs tbody').on( 'click', '.revert-modification', function () {
        let data = $(this).parents('tr')[0].getElementsByTagName('td');
        if (confirm("Voulez-vous annuler: " + data[1].innerText + ' ' + data[2].innerText + ' ?')){
            revertModification("water_element", data[0].innerText);
        } else {}
    } );
    $('#datatable-water_element tbody').on( 'click', '.accept-modification', function () {
        let data = $(this).parents('tr')[0].getElementsByTagName('td');
        acceptModification(data);
    } );
    prettifyHeader('logs');
}

function getLogsTableConfiguration(dataURL){
    let config = {
        lengthMenu: [
            [ 10, 25, 50, -1 ],
            [ '10', '25', '50', 'Tout afficher' ]
        ],
        dom: 'Bfrtip',
        buttons: [
            'pageLength'
        ],
        "searching": false,
        "sortable": true,
        "processing": true,
        "serverSide": true,
        "responsive": true,
        "autoWidth": true,
        scrollX:        true,
        scrollCollapse: true,
        paging:         true,
        fixedColumns:   {
            leftColumns: 1,
            rightColumns: 1
        },
        "columnDefs": [
            {
                "targets": -1,
                "data": null,
                "orderable": false,
                "defaultContent": getLogsActionButtonsHTML(),
            }
            ],
        "language": getDataTableFrenchTranslation(),
        "ajax": {
            url: dataURL
        }
    };
    return config;
}

function getLogsActionButtonsHTML(){
    return '<div class="center"><a style="cursor:pointer;" class="accept-modification fas fa-check-square"></a>' +
            '&nbsp&nbsp&nbsp&nbsp' + // Non-breaking spaces to avoid clicking on the wrong icon
            '<a style="cursor:pointer;" class="revert-modification far fa-times-circle"></a></div>'
}
