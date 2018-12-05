function drawWaterElementTable(withManagers, withActions){
    let baseURL = location.protocol+'//'+location.hostname+(location.port ? ':'+location.port: '');
    let dataURL = baseURL + "/api/table/?name=water_element";
    console.log("Request data from: " + dataURL);
    $('#datatable-ajax').DataTable(getWaterDatatableConfiguration(dataURL, withManagers, withActions));

    let table = $('#datatable-ajax').DataTable();
    $('#datatable-ajax tbody').on( 'click', 'tr', function () {
        if ( $(this).hasClass('selected') ) {
            $(this).removeClass('selected');
        }
        else {
            table.$('tr.selected').removeClass('selected');
            $(this).addClass('selected');
        }
    });

    $('#datatable-ajax tbody').on( 'click', '.remove-row', function () {
        let data = $(this).parents('tr')[0].getElementsByTagName('td');
        if (confirm("Voulez-vous supprimer: " + data[1].innerText + ' ' + data[2].innerText + ' ?')){
            removeElement("water_element", data[0].innerText);
        } else {}
    } );
    $('#datatable-ajax tbody').on( 'click', '.edit-row', function () {
        let data = $(this).parents('tr')[0].getElementsByTagName('td');
        editElement(data);
    } );

    prettifyHeader();
}

function getWaterDatatableConfiguration(dataURL, withManagers, withActions){
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
        "columnDefs": [
            {
                "targets": -1,
                "data": null,
                "defaultContent": getActionButtonsHTML(),
            },
            {
                "targets": -2,
                "defaultContent": "Pas de gestionnaire",
                "visible": withManagers,
            }
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
            if(!withActions) // Hide last column content if we don't need the actions
                $('td', row).eq(8).addClass('hidden');
        },
        "initComplete": function(settings, json){
            // Removes the last column (both header and body) if we cannot edit or if required by withAction argument
            console.log(json['editable']);
            if(!withActions || !(json.hasOwnProperty('editable') && json['editable'])){
                $("#datatable-ajax th:last-child, #datatable-ajax td:last-child").addClass("hidden");
                $("#datatable-ajax_wrapper tr:last-child th:last-child").addClass("hidden");
            }
        }
    };
    return config;
}