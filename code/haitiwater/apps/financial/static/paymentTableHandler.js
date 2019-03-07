function drawPaymentTable() {
    let baseURL = location.protocol+'//'+location.hostname+(location.port ? ':'+location.port: '');
    let dataURL = baseURL + "/api/table/?name=payment&user=none";

    let datatable = $('#datatable-payment');

    let table = datatable.DataTable(getPaymentDatatableConfiguration(dataURL));

    datatable.find('tbody').on( 'click', '.remove-row', function () {
        let data = table.row($(this).closest('tr')).data();
        if (confirm("Voulez-vous supprimer: " + data[0] + ' ?')){
            let consumerIdParameter = '&id_consumer=' + $('#input-payment-id-consumer');
            removeElement("payment", data[0], consumerIdParameter );
        } else {}
    } );
    datatable.find('tbody').on( 'click', '.edit-row', function () {
        let data = table.row($(this).closest('tr')).data();
        setupModalPaymentEdit(data);
    } );

    prettifyHeader('payment');
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
        "columnDefs": [
            {
                "targets": -1,
                "data": null,
                "orderable": false,
                "defaultContent": getActionButtonsHTML("modal-payment"),
            }
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
                if(xhr.status !== 200) { // Avoid first load error
                    console.log(xhr + '\n' + error + '\n' + thrown);
                    new PNotify({
                        title: 'Échec du téléchargement!',
                        text: "Les données des paiements n'ont pas pu être téléchargées",
                        type: 'failure'
                    });
                }
            }
        },
    };
    return config;
}
