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
 * Request the removal of element # id in table
 * @param table a String containing the table name
 * @param id an integer corresponding to the primary key of the element to remove
 */
function removeElement(table, id){
    let baseURL = location.protocol+'//'+location.hostname+(location.port ? ':'+location.port: '');
    let postURL = baseURL + "/api/remove/?table=" + table + "&id=" + id;
    let xhttp = new XMLHttpRequest();
    xhttp.open("POST", postURL, true);
    xhttp.onreadystatechange = function() {
        if(xhttp.readyState === 4) {
            if (xhttp.status !== 200) {
                console.log("POST error on remove element");
                new PNotify({
                    title: 'Échec!',
                    text: "L'élement n'a pas pu être supprimé",
                    type: 'error'
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
    xhttp.send()
}

/**
 *
 * @returns {string} containing edit and remove buttons HTML code
 */
function getActionButtonsHTML(){
    return '<div class="center"><a href="#modalForm" class="modal-with-form edit-row fa fa-pen"></a>' +
            '&nbsp&nbsp&nbsp&nbsp' + // Non-breaking spaces to avoid clicking on the wrong icon
            '<a style="cursor:pointer;" class="on-default remove-row fa fa-trash"></a></div>'
}

/**
 * Add placeholder and CSS class in the search field
 */
function prettifyHeader(){
    $('#datatable-ajax_filter').find('input').addClass("form-control");
    $('#datatable-ajax_filter').find('input').attr("placeholder", "Recherche");
    $('#datatable-ajax_filter').css("min-width", "300px");
}