$(document).ready(function() {
    // Draw the water element table without the managers
    drawLogsHistoryTable();
});


//Formatting function for row details
function format ( d ) {
    // d is the original data object for the row
    return d.details;
}

function drawLogsHistoryTable(){
    let baseURL = location.protocol+'//'+location.hostname+(location.port ? ':'+location.port: '');
    let dataURL = baseURL + "/api/table/?name=logs_history";
    console.log("Request data from: " + dataURL);
    let table = $('#datatable-logs-history').DataTable(getLogsHistoryTableConfiguration(dataURL));

    $('#datatable-logs-history tbody').on( 'click', 'tr td:not(:last-child)', function () {
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
    prettifyHeader('logs-history');
}

function getLogsHistoryTableConfiguration(dataURL){
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
            { "data": "action" }
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
        pagingType: 'full_numbers',
        fixedColumns:   {
            leftColumns: 1,
            rightColumns: 1
        },
        "language": getDataTableFrenchTranslation(),
        "ajax": {
            url: dataURL,
            error: function (xhr, error, thrown) {
                console.log(xhr + '\n' + error + '\n' + thrown);
                $('#datatable-logs-history_wrapper').hide();
                new PNotify({
                    title: 'Échec du téléchargement!',
                    text: "Les données de la table des anciens historiques n'ont pas pu être téléchargées",
                    type: 'failure'
                });
            }
        }
    };
    return config;
}