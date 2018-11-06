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
        "language": {
            "sProcessing":     "Chargement...",
            "sSearch":         "",
            "sLengthMenu":     "Afficher _MENU_ &eacute;l&eacute;ments",
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
} );

/**
 * Tell the window to display a horizontal scroll if the entire table cannot be displayed.
 */
resizeWraperIfNeeded()
function resizeWraperIfNeeded() {
    if ($('#datatable-ajax_wrapper').outerWidth() > 500){
        $('#datatable-ajax_wrapper').css("overflow-x","hidden");
    } else {
        $('#datatable-ajax_wrapper').css("overflow-x","auto");
    }
}
$( window ).resize(function() {
    console.log("Inside resize function");
    console.log($('#datatable-ajax_wrapper').outerWidth());
    resizeWraperIfNeeded()
});