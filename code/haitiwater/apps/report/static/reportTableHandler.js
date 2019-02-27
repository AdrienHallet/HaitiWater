//Formatting function for row details
function format ( d ) {
    let outletAsHTMLList = '<ul>';
    for(let i = 0; i < d.details.length; i++){
        outletAsHTMLList += '<li>' + d.details[i].name + '</li>'
    }
    outletAsHTMLList += '</ul>';

    // d is the original data object for the row
    return 'Rapport du ' + d.date +
        outletAsHTMLList +
        '<br><button id="button-modal-edit-report" type="button" class="btn" href="#modalMonthlyReportEdit">Modifier</button>';
}

function drawReportTable(){
    let baseURL = location.protocol+'//'+location.hostname+(location.port ? ':'+location.port: '');
    let dataURL = baseURL + "/api/table/?name=report";
    console.log("Request data from: " + dataURL);
    let table = $('#datatable-report').DataTable(getReportDatatableConfiguration(dataURL));

    $('#datatable-report tbody').on( 'click', 'tr', function (event) {
        let tr = $(this).closest('tr');
        let row = table.row(tr);

        if (row.child.isShown()) {
            // This row is already open - close it
            row.child.hide();
            tr.removeClass('shown');
        }
        else {
            if($(event.target).is('button')) { // The click is on the button
                showModal('#button-modal-edit-report');
                return;
            } else { // The click is somewhere in the details
                setupModalMonthlyReportEdit(row.data());
            }
            // Open this row
            row.child( format(row.data()) ).show();
            tr.addClass('shown');
        }
    });
}

function getReportDatatableConfiguration(dataURL){
    let config = {
        sortable: false,
        searching: false,
        paging: false,
        processing: true,
        serverSide: true,
        responsive: true,
        autoWidth: true,
        scrollX:        true,
        scrollCollapse: true,
        columns: [
            {
                data: "id",
                sortable: false,
            },
            {
                data: "date",
                sortable: false,
            },
        ],
        language: getDataTableFrenchTranslation(),
        ajax: {
            url: dataURL,
            error: function (xhr, error, thrown) {
                console.log(xhr + '\n' + error + '\n' + thrown);
                $('#datatable-report_wrapper').hide();
                new PNotify({
                    title: 'Échec du téléchargement!',
                    text: "Les données de la table n'ont pas pu être téléchargées",
                    type: 'failure'
                });
            }
        },
    };
    return config;
}
