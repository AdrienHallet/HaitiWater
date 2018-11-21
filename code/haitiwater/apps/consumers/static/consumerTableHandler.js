/**
 * Custom Table Handler
 * Used to prettify the table and make it respond to custom input and commands
 *
 */
$(document).ready(function() {
    let baseURL = location.protocol+'//'+location.hostname+(location.port ? ':'+location.port: '');
    let dataURL = baseURL + "/api/table/?name=consumer";
    console.log(dataURL);
    $('#datatable-ajax').DataTable(getDatatableConfiguration(dataURL));

    let table = $('#datatable-ajax').DataTable();
    $('#datatable-ajax tbody').on('click', 'tr', function () {
        if ($(this).hasClass('selected')) {
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
            removeElement(data[0]);
        } else {}
    } );
    $('#datatable-ajax tbody').on( 'click', '.edit-row', function () {
        let data = $(this).parents('tr')[0].getElementsByTagName('td');
        editElement(data);
    } );

    prettifyHeader();
});

function editElement(data){
    if(data){
        setupModalEdit(data);
    } else {
        new PNotify({
            title: 'Échec!',
            text: "L'élément ne peut être récupéré (tableHandler.js)",
            type: 'error'
        });
    }
}

/**
 * Add placeholder and CSS class in the search field
 */
function prettifyHeader(){
    $('#datatable-ajax_filter').find('input').addClass("form-control");
    $('#datatable-ajax_filter').find('input').attr("placeholder", "Recherche");
    $('#datatable-ajax_filter').css("min-width", "300px");
}

function getDatatableConfiguration(dataURL){
    let config = {
        "sortable": true,
        "processing": false,
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
            }],
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
            "semptyTable": "Aucune donn&eacute;e disponible dans le tableau",
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
        "initComplete": function(settings, json){
            // Removes the last column (both header and body) if we cannot edit the table
            console.log(json.hasOwnProperty('editable'));
            console.log(json['editable']);
            if(!(json.hasOwnProperty('editable') && json['editable'])){
                $('#datatable-ajax').find('tr:last-child th:last-child, td:last-child').remove();
            }
        }
    };
    return config;
}

function onAjaxFailure(xhr, error, thrown){
    new PNotify({
        title: 'Échec!',
        text: 'Le contenu de la table n\'a pu être récupéré',
        type: 'fail'
    });
    console.log(xhr);
    console.log(error);
    console.log(thrown);
}

function getActionButtonsHTML(){
    return '<div class="center"><a href="#modalForm" class="modal-with-form edit-row fa fa-pen"></a>' +
            '&nbsp&nbsp&nbsp&nbsp' + // Non-breaking spaces to avoid clicking on the wrong icon
            '<a style="cursor:pointer;" class="on-default remove-row fa fa-trash"></a></div>'
}