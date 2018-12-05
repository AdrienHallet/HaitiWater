function drawManagersTable(){
    let baseURL = location.protocol+'//'+location.hostname+(location.port ? ':'+location.port: '');
    let dataURL = baseURL + "/api/table/?name=managers";
    console.log("Request data from: " + dataURL);
    $('#datatable-managers').DataTable(getDatatableConfiguration(dataURL));

    let table = $('#datatable-managers').DataTable();
    $('#datatable-managers tbody').on( 'click', 'tr', function () {
        if ( $(this).hasClass('selected') ) {
            $(this).removeClass('selected');
        }
        else {
            table.$('tr.selected').removeClass('selected');
            $(this).addClass('selected');
        }
    });

    $('#datatable-managers tbody').on( 'click', '.remove-row', function () {
        let data = $(this).parents('tr')[0].getElementsByTagName('td');
        if (confirm("Voulez-vous supprimer: " + data[1].innerText + ' ' + data[2].innerText + ' ?')){
            removeElement("managers", data[0].innerText);
        } else {}
    } );
    $('#datatable-managers tbody').on( 'click', '.edit-row', function () {
        let data = $(this).parents('tr')[0].getElementsByTagName('td');
        editElement(data);
    } );

    prettifyManagersHeader();
}
/**
 * Add placeholder and CSS class in the search field
 */
function prettifyManagersHeader(){
    $('#datatable-managers_filter').find('input').addClass("form-control");
    $('#datatable-managers_filter').find('input').attr("placeholder", "Recherche");
    $('#datatable-managers_filter').css("min-width", "300px");
}

function getDatatableConfiguration(dataURL){
    let config = {
        "sortable": true,
        "processing": true,
        "serverSide": true,
        "responsive": false,
        "autoWidth": false,
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
                "defaultContent": getActionButtonsHTML(),
            },
            ],
        "language": {
            "sProcessing": "Chargement...",
            "sSearch": "",
            "sLengthMenu": "_MENU_ &eacute;l&eacute;ments",
            "sInfo": "", //"Affichage de l'&eacute;lement _START_ &agrave; _END_ sur _TOTAL_ &eacute;l&eacute;ments",
            "sInfoEmpty": "Affichage de l'&eacute;lement 0 &agrave; 0 sur 0 &eacute;l&eacute;ments",
            "sInfoFiltered": "(filtr&eacute; de _MAX_ &eacute;l&eacute;ments au total)",
            "sInfoPostFix": "",
            "sLoadingRecords": "Chargement en cours...",
            "sZeroRecords": "Aucun &eacute;l&eacute;ment &agrave; afficher",
            "sEmptyTable": "Aucune donn&eacute;e disponible dans le tableau",
            "oPaginate": {
                "sFirst": "Premier",
                "sPrevious": "Pr&eacute;c&eacute;dent",
                "sNext": "Suivant",
                "sLast": "Dernier"
            },
            "oAria": {
                "sSortAscending": ": activer pour trier la colonne par ordre croissant",
                "sSortDescending": ": activer pour trier la colonne par ordre d&eacute;croissant"
            }
        },
        "ajax": {
            url: dataURL
        },

        //Callbacks on fetched data
        "createdRow": function (row, data, index) {
            $('td', row).eq(5).addClass('text-center');
            $('td', row).eq(6).addClass('text-center');
        },
        "initComplete": function(settings, json){
            // Removes the last column (both header and body) if we cannot edit the table
            if(!(json.hasOwnProperty('editable') && json['editable'])){
                $('#datatable-ajax').find('tr:last-child th:last-child, td:last-child').remove();
            }
        }
    };
    return config;
}