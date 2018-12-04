/**
 * Hide all the error messages from start.
 * It is better to hide them than to append HTML with JS
 */
window.onload = function() {
    let buttons = document.getElementsByClassName("error"),
        len = buttons !== null ? buttons.length : 0,
        i = 0;
    for(i; i < len; i++) {
        buttons[i].className += " hidden";
    }
};

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
    let postURL = baseURL + "/api/remove/";
    let xhttp = new XMLHttpRequest();
    xhttp.open("POST", postURL, true);
    xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
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
                    text: 'Élément supprimé avec succès',
                    type: 'success'
                });
                drawDataTable();
            }
        }
    };
    xhttp.send("table=" + table + "&id=" + id);
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

/**
 * Send a post request to server and handle it
 */
function postNewRow(){
    let request = validateForm();
    if(!request){
        // Form is not valid (missing/wrong fields)
        return false;
    }
    let baseURL = location.protocol+'//'+location.hostname+(location.port ? ':'+location.port: '');
    let postURL = baseURL + "/api/add/";
    let xhttp = new XMLHttpRequest();
    xhttp.open("POST", postURL, true);
    xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    xhttp.onreadystatechange = function() {
        if(xhttp.readyState !== 4) {
            if (xhttp.status !== 200) {
                document.getElementById("form-error").className = "alert alert-danger";
                document.getElementById("form-error-msg").innerHTML = xhttp.status + ': ' + xhttp.statusText;
            } else {
                document.getElementById("form-error").className = "alert alert-danger hidden"; // hide old msg
                dismissModal();
                new PNotify({
                    title: 'Succès!',
                    text: 'Élément ajouté avec succès',
                    type: 'success'
                });
                drawDataTable();
            }
        }
    };
    xhttp.send(request)
}

/**
 * Send a post request to server and handle it
 */
function postEditRow(){
    let request = validateForm();
    if(!request){
        // Form is not valid (missing/wrong fields)
        return false;
    }
    let baseURL = location.protocol+'//'+location.hostname+(location.port ? ':'+location.port: '');
    let postURL = baseURL + "/api/edit/?" + request;
    let xhttp = new XMLHttpRequest();
    xhttp.open("POST", postURL, true);
    xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    xhttp.onreadystatechange = function() {
        if(xhttp.readyState !== 4) {
            if (xhttp.status !== 200) {
                if (xhttp.responseText) {
                    console.log("POST error on new element");
                    document.getElementById("form-error").className = "alert alert-danger";
                    document.getElementById("form-error-msg").innerHTML = xhttp.responseText;
                }
            } else {
                document.getElementById("form-error").className = "alert alert-danger hidden"; // hide old msg
                dismissModal();
                new PNotify({
                    title: 'Succès!',
                    text: 'Élément édité avec succès',
                    type: 'success'
                });
                drawDataTable();
            }
        }
    };
    xhttp.send(request)
}