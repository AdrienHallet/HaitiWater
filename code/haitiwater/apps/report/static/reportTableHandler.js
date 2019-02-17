function drawReportTable(){
    let baseURL = location.protocol+'//'+location.hostname+(location.port ? ':'+location.port: '');
    let dataURL = baseURL + "/api/table/?name=report";
    console.log("Request data from: " + dataURL);
    $('#datatable-report').DataTable(getReportDatatableConfiguration(dataURL));

    let table = $('#datatable-report').DataTable();
    $('#datatable-report tbody').on( 'click', 'tr', function () {
        if ( $(this).hasClass('selected') ) {
            $(this).removeClass('selected');
        }
        else {
            table.$('tr.selected').removeClass('selected');
            $(this).addClass('selected');
        }
    });

    $('#datatable-report tbody').on( 'click', '.edit-row', function () {
        let data = $(this).parents('tr')[0].getElementsByTagName('td');
        editElement(data);
    } );
}

function getReportDatatableConfiguration(dataURL){
    let config = {
        "sortable": true,
        "processing": true,
        "serverSide": true,
        "responsive": true,
        "autoWidth": false,
        scrollX:        true,
        scrollCollapse: true,
        "columnDefs": [
            {
                "targets": -1,
                "data": null,
                "orderable": false,
                "defaultContent": "TODO",
            },
            ],
        "language": getDataTableFrenchTranslation(),
        "ajax": {
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
