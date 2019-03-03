/**
 * Custom Table Handler
 * Used to prettify the table and make it respond to custom input and commands
 *
 */
function drawConsumerTable() {
    let baseURL = location.protocol+'//'+location.hostname+(location.port ? ':'+location.port: '');
    let dataURL = baseURL + "/api/table/?name=consumer";
    console.log(dataURL);

    let datatable = $('#datatable-consumer');

    datatable.DataTable(getDatatableConfiguration(dataURL));

    let table = datatable.DataTable();
    datatable.find('tbody').on('click', 'tr', function () {
        if ($(this).hasClass('selected')) {
            $(this).removeClass('selected');
        }
        else {
            table.$('tr.selected').removeClass('selected');
            $(this).addClass('selected');
        }
    });

    datatable.find('tbody').on( 'click', '.remove-row', function () {
        let data = $(this).parents('tr')[0].getElementsByTagName('td');
        if (confirm("Voulez-vous supprimer: " + data[1].innerText + ' ' + data[2].innerText + ' ?')){
            removeElement("consumer", data[0].innerText);
        } else {}
    } );
    datatable.find('tbody').on( 'click', '.edit-row', function () {
        let data = $(this).parents('tr')[0].getElementsByTagName('td');
        setupModalConsumerEdit(data);
    } );

    prettifyHeader('consumer');
}

function getDatatableConfiguration(dataURL){
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
                    columns: [0,1,2,3,4,5,6,7,8,9],
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
        fixedColumns:   {
            leftColumns: 1,
            rightColumns: 1
        },
        "columnDefs": [{
                "targets": -1,
                "data": null,
                "orderable": false,
                "defaultContent": getActionButtonsHTML("modalConsumer"),
            }],
        "language": getDataTableFrenchTranslation(),
        "ajax": {
            url: dataURL,
            error: function (xhr, error, thrown) {
                console.log(xhr + '\n' + error + '\n' + thrown);
                $('#datatable-ajax_wrapper').hide();
                new PNotify({
                    title: 'Échec du téléchargement!',
                    text: "Les données de la table n'ont pas pu être téléchargées",
                    type: 'failure'
                });
            }
        },

        //Callbacks on fetched data
        "createdRow": function (row, data, index) {
            if ($("#datatable-consumer th:last-child, #datatable-ajax td:last-child").hasClass("hidden")){
                $('td', row).eq(10).addClass('hidden');
            }
        },

        "initComplete": function(settings, json){
            // Removes the last column (both header and body) if we cannot edit
            if(!(json.hasOwnProperty('editable') && json['editable'])){
                $("#datatable-consumer th:last-child, #datatable-ajax td:last-child").addClass("hidden");
                $("#datatable-ajax_wrapper tr:last-child th:last-child").addClass("hidden");
            }
        }
    };
    return config;
}
