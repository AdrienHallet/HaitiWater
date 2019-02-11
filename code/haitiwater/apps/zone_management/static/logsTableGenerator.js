$(document).ready(function() {
    // Draw the water element table without the managers
    drawLogTable();
});


//Formatting function for row details
function format ( d ) {
    // d is the original data object for the row
    return 'Détails : ' + d.details;
}

function drawLogTable(){
    let baseURL = location.protocol+'//'+location.hostname+(location.port ? ':'+location.port: '');
    let dataURL = baseURL + "/api/table/?name=logs";
    console.log("Request data from: " + dataURL);
    $('#datatable-logs').DataTable(getLogsTableConfiguration(dataURL));
    let table = $('#datatable-logs').DataTable();

    $('#datatable-water_element tbody').on( 'click', 'tr', function () {
        var tr = $(this);
        var row = table.row( tr );

        if ( row.child.isShown() ) {
            // This row is already open - close it
            row.child.hide();
            tr.removeClass('shown');
        }
        else {
            // Open this row
            row.child( format(row.data()) ).show();
            tr.addClass('shown');
        }
    });

    $('#datatable-logs tbody').on( 'click', '.revert-modification', function () {
        let data = $(this).parents('tr')[0].getElementsByTagName('td');
        if (confirm("Voulez-vous annuler: " + data[1].innerText + ' ' + data[2].innerText + ' ?')){
            transactionAction('revert', data[0].innerText);
        } else {}
    } );
    $('#datatable-water_element tbody').on( 'click', '.accept-modification', function () {
        let data = $(this).parents('tr')[0].getElementsByTagName('td');
        transactionAction('accept', data[0].innerText);
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
        "columns": [
            { "data": "id" },
            { "data": "time" },
            { "data": "type" },
            { "data": "user" },
            { "data": "summary" },
            {
                "className":      'actions',
                "orderable":      false,
                "data":           null,
                "defaultContent": getLogsActionButtonsHTML()
            }
        ],
        "order": [[1, 'asc']]
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

transactionAction(action, id){
    let postURL = "../../api/log/?action=" + action + "&id=" + id;
    let xhttp = new XMLHttpRequest();
    xhttp.open("POST", postURL, true);
    xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    xhttp.onreadystatechange = function() {
        if(xhttp.readyState === 4) {
            if (xhttp.status !== 200) {
                console.log(this);
                new PNotify({
                    title: 'Échec!',
                    text: "L'action n'a pas pu être annulée.",
                    type: 'error'
                });
            } else {
                drawDataTable('logs');
            }
        }
    };
    xhttp.send();
}
