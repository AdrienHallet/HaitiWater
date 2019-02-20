

function drawTicketTable(){
    let baseURL = location.protocol+'//'+location.hostname+(location.port ? ':'+location.port: '');
    let dataURL = baseURL + "/api/table/?name=ticket";
    console.log("Request data from: " + dataURL);
    $('#datatable-ticket').DataTable(getTicketDatatableConfiguration(dataURL));

    $('#datatable-ticket tbody').on( 'click', '.remove-row', function () {
        let data = $(this).parents('tr')[0].getElementsByTagName('td');
        if (confirm("Voulez-vous supprimer: " + data[1].innerText + ' ' + data[2].innerText + ' ?')){
            removeElement("ticket", data[0].innerText);
        } else {}
    } );
    $('#datatable-ticket tbody').on( 'click', '.edit-row', function () {
        let data = $(this).parents('tr')[0].getElementsByTagName('td');
        editElement(data);
    } );
    prettifyHeader('ticket');
}

function getTicketDatatableConfiguration(dataURL){
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
                    columns: [0,1,2,3,4,5,6,7],
                },
            },
            'pageLength'
        ],
        "sortable": true,
        "processing": true,
        "serverSide": true,
        "responsive": true,
        "autoWidth": true,
        scrollX:        true,
        scrollCollapse: true,
        paging:         true,
        "columnDefs": [
            {
                "targets": -1,
                "data": null,
                "orderable": false,
                "defaultContent": getActionButtonsHTML('modalProblemReport'),
            },
            ],
        "language": getDataTableFrenchTranslation(),
        "ajax": {
            url: dataURL,
            error: function (xhr, error, thrown) {
                console.log(xhr + '\n' + error + '\n' + thrown);
                $('#datatable-ticket_wrapper').hide();
                new PNotify({
                    title: 'Échec du téléchargement!',
                    text: "Les données de la table n'ont pas pu être téléchargées",
                    type: 'failure'
                });
            }
        },

        //Callbacks on fetched data
        "createdRow": function (row, data, index, cells) {
            let imageURL = '../static/' + data[7];
            if (imageURL !== 'none'){
                let commentDom = $('td', row).eq(5);
                let comment = commentDom.text();

                commentDom.html('<i class="far fa-image" title="Cliquez pour voir l\'image"></i>' + comment);
                commentDom.on('click', function(){
                    $.magnificPopup.open({
                        type: 'image',
                        items: {
                        src: imageURL
                        },
                    });
                })
            }
        }
    };

    return config;
}