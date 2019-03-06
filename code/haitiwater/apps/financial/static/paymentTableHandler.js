function setPaymentTableURL(userID){
    let baseURL = location.protocol+'//'+location.hostname+(location.port ? ':'+location.port: '');
    let dataURL = baseURL + "/api/table/?name=payment&user=" + userID;
    $('#datatable-payment').DataTable().ajax.url(dataURL).load();
}

function drawPaymentTable() {
    let baseURL = location.protocol+'//'+location.hostname+(location.port ? ':'+location.port: '');
    let dataURL = baseURL + "/api/table/?name=payment&user=none";

    let datatable = $('#datatable-payment');

    datatable.DataTable(getPaymentDatatableConfiguration(dataURL));

    prettifyHeader('consumer');
}

function getPaymentDatatableConfiguration(dataURL){
    let config = {
        lengthMenu: [
            [ 10, 25, 50, -1 ],
            [ '10', '25', '50', 'Tout afficher' ]
        ],
        dom: 'Bfrtip',
        buttons: [
            {
                extend: 'print',
                exportOptions: {
                    columns: [0,1,2],
                },
            },
            'pageLength'
        ],
        "sortable": true,
        "processing": false,
        "serverSide": true,
        "responsive": true,
        "autoWidth": true,
        scrollX:        true,
        scrollCollapse: true,
        paging:         true,
        "language": getDataTableFrenchTranslation(),
        "ajax": {
            url: dataURL,
            error: function (xhr, error, thrown) {
                console.log(xhr + '\n' + error + '\n' + thrown);
                $('#datatable-payment_wrapper').hide();
                new PNotify({
                    title: 'Échec du téléchargement!',
                    text: "Les données des paiements n'ont pas pu être téléchargées",
                    type: 'failure'
                });
            }
        },
    };
    return config;
}
