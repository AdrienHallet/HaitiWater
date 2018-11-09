/**
 * Custom Table Handler
 * Used to prettify the table and make it respond to custom input and commands
 *
 */
$(document).ready(function() {
    let baseURL = location.protocol+'//'+location.hostname+(location.port ? ':'+location.port: '');
    let dataURL = baseURL + "/api/table/?name=water_element";
    console.log(dataURL);
    $('#datatable-ajax').DataTable({
        "sortable": true,
        "processing": false,
        "serverSide": true,
        "responsive": true,
        "autoWidth": false,
        "columnDefs": [{
            "targets": -1,
            "data": null,
            "defaultContent": getActionButtonsHTML(),
        }],
        "language": {
            "sProcessing":     "Chargement...",
            "sSearch":         "",
            "sLengthMenu":     "_MENU_ &eacute;l&eacute;ments",
            "sInfo":           "", //"Affichage de l'&eacute;lement _START_ &agrave; _END_ sur _TOTAL_ &eacute;l&eacute;ments",
            "sInfoEmpty":      "Affichage de l'&eacute;lement 0 &agrave; 0 sur 0 &eacute;l&eacute;ments",
            "sInfoFiltered":   "(filtr&eacute; de _MAX_ &eacute;l&eacute;ments au total)",
            "sInfoPostFix":    "",
            "sLoadingRecords": "Chargement en cours...",
            "sZeroRecords":    "Aucun &eacute;l&eacute;ment &agrave; afficher",
            "sEmptyTable":     "Aucune donn&eacute;e disponible dans le tableau",
            "oPaginate": {
                "sFirst":      "Premier",
                "sPrevious":   "Pr&eacute;c&eacute;dent",
                "sNext":       "Suivant",
                "sLast":       "Dernier"
            },
            "oAria": {
                "sSortAscending":  ": activer pour trier la colonne par ordre croissant",
                "sSortDescending": ": activer pour trier la colonne par ordre d&eacute;croissant"
            }
        },
        "ajax": dataURL,

        //Callbacks on fetched data
        "createdRow": function ( row, data, index ) {
            $('td', row).eq(5).addClass('text-center');
            $('td', row).eq(6).addClass('text-center');
        }
    });

    let table = $('#example').DataTable();
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
            removeElement(data[0]);
        } else {}
    } );

    resizeWraperIfNeeded();
    prettifyHeader();
});

/**
 * Remove an element from the water_element database
 * @param id the ID of the element to remove
 */
function removeElement(id){
    let baseURL = location.protocol+'//'+location.hostname+(location.port ? ':'+location.port: '');
    let postURL = baseURL + "/api/remove";
    let xhttp = new XMLHttpRequest();
    xhttp.open("POST", postURL, true);
    xhttp.onreadystatechange = function() {
        if(xhttp.readyState === 4) {
            if (xhttp.status !== 200) {
                console.log("POST error on remove element");
                new PNotify({
                    title: 'Échec!',
                    text: "L'élement n'a pas pu être supprimé",
                    type: 'alert'
                });
            } else {
                new PNotify({
                    title: 'Succès!',
                    text: 'Élément ajouté avec succès',
                    type: 'success'
                });
                $('#datatable-ajax').DataTable().reload();
            }
        }
    };
    xhttp.send('?table=water_element&id='+id)
}

/**
 * Add placeholder and CSS class in the search field
 */
function prettifyHeader(){
    $('#datatable-ajax_filter').find('input').addClass("form-control");
    $('#datatable-ajax_filter').find('input').attr("placeholder", "Recherche");
    $('#datatable-ajax_filter').css("min-width", "400px");
}

/**
 * Tell the window to display a horizontal scroll if the entire table cannot be displayed.
 */
function resizeWraperIfNeeded() {
    if ($('#datatable-ajax_wrapper').outerWidth() > 600){ //Adjust value to table length
        $('#datatable-ajax_wrapper').css("overflow-x","hidden");

    } else {
        $('#datatable-ajax_wrapper').css("overflow-x","auto");
    }
}
$( window ).resize(function() {
    resizeWraperIfNeeded()
});

function getActionButtonsHTML(){
    return '<div class="center"><a style="cursor:pointer;" class="on-default edit-row">' +
                '<i class="fa fa-pen"></i></a>    ' +
            '<a style="cursor:pointer;" class="on-default remove-row">' +
                '<i class="fa fa-trash"></i></a></div>'
}