$(document).ready(function() {
    // Draw the water element table without the managers
    drawLogTable();
});


//Formatting function for row details
function format ( d ) {
    // d is the original data object for the row
    return d.details;
}

function drawLogTable(){
    let baseURL = location.protocol+'//'+location.hostname+(location.port ? ':'+location.port: '');
    let dataURL = baseURL + "/api/table/?name=logs";
    console.log("Request data from: " + dataURL);
    $('#datatable-logs').DataTable(getLogsTableConfiguration(dataURL));
    let table = $('#datatable-logs').DataTable();

    $('#datatable-logs tbody').on( 'click', 'tr td:not(:last-child)', function () {
        var tr = $(this).closest('tr');
        var row = table.row(tr);
        console.log(row.data());

        if (row.child.isShown()) {
            // This row is already open - close it
            row.child.hide();
            tr.removeClass('shown');
        }
        else {
            // Open this row
            console.log(row.data());
            row.child( format(row.data()) ).show();
            tr.addClass('shown');
        }
    });

    $('#datatable-logs tbody').on( 'click', '.revert-modification', function () {
        let data = table.row($(this).closest('tr')).data();
        revertModification(data.id);
    } );
    $('#datatable-logs tbody').on( 'click', '.accept-modification', function () {
        let data = table.row($(this).closest('tr')).data();
        acceptModification(data.id);
    } );
    prettifyHeader('logs');
}

function revertModification(elementID){
    let url = '../../api/log?action=revert&id=' + elementID;
    requestHandler(url);
}

function acceptModification(elementID){
    let url = '../../api/log?action=accept&id=' + elementID;
    requestHandler(url);
}

function requestHandler(url){
    let xhttp = new XMLHttpRequest();

    xhttp.onreadystatechange = function(){
        if (this.readyState == 4 && this.status == 200) {
            drawLogTable();
        }
        else if (this.readyState == 4){
            console.log(this);
            new PNotify({
                title: 'Échec!',
                text: "Opération impossible: " + this.statusText,
                type: 'error'
            });
        }
    }

    xhttp.open('POST', url, true);
    xhttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhttp.send();
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
        "order": [[1, 'asc']],
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
