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

function drawDataTable(tableName){
    $('#datatable-' + tableName).DataTable().draw();
    if (tableName === 'payment'){ // Should go in callback called by postNewRow
        requestFinancialDetails($('#input-payment-id-consumer').val());
    }
}

/**
 * Request the removal of element # id in table
 * @param table a String containing the table name
 * @param id an integer corresponding to the primary key of the element to remove
 */
function removeElement(table, id, otherParameters){
    let baseURL = location.protocol+'//'+location.hostname+(location.port ? ':'+location.port: '');
    let postURL = baseURL + "/api/remove/";
    let xhttp = new XMLHttpRequest();
    xhttp.open("POST", postURL, true);
    xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    xhttp.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
    xhttp.onreadystatechange = function() {
        if(xhttp.readyState === 4) {
            if (xhttp.status !== 200) {
                console.log("POST error on remove element");
                new PNotify({
                    title: 'Échec!',
                    text: xhttp.responseText,
                    type: 'error'
                });
            } else {
                new PNotify({
                    title: 'Succès!',
                    text: 'Élément supprimé avec succès',
                    type: 'success'
                });
                drawDataTable(table);
            }
        }
    };
    if (typeof otherParameters === 'undefined') { otherParameters = ''; }
    xhttp.send("table=" + table + "&id=" + id + otherParameters);
}

/**
 *
 * @returns {string} containing edit and remove buttons HTML code
 */
function getActionButtonsHTML(modalName){
    return '<div class="center"><a href="#'+ modalName + '" class="modal-with-form edit-row fa fa-pen" title="Editer"></a>' +
            '&nbsp&nbsp&nbsp&nbsp' + // Non-breaking spaces to avoid clicking on the wrong icon
            '<a style="cursor:pointer;" class="on-default remove-row fa fa-trash" title="Supprimer"></a></div>'
}

function hideFormErrorMsg(table){
    $('#form-' + table + '-error').addClass('hidden');
}

/**
 * Add placeholder and CSS class in the search field
 */
function prettifyHeader(tableName){
    let searchField = $('#datatable-' + tableName + '_filter');
    searchField.find('input').addClass("form-control");
    searchField.find('input').attr("placeholder", "Recherche");

    let wrapper = $('#datatable-'+ tableName + '_wrapper');
    let buttons = wrapper.find('.dt-buttons');

    buttons.addClass('hidden');
    buttons.find('.buttons-print').addClass('hidden');

    // Link the custom print button to the DataTable one (hidden)
    let print = wrapper.find('.buttons-print');
    $('#print-' + tableName).on('click', function(){
        print.trigger('click');
    });

    let pageLength = wrapper.find('.buttons-page-length');
    $('#' + tableName + '-options').on('click', function(){
        (buttons.hasClass('hidden') ? buttons.removeClass('hidden') : buttons.addClass('hidden'))
    })

}

function getRequest(table){
    switch(table){
        case 'manager':
            return validateManagerForm();
        case 'zone':
            return validateZoneForm();
        case 'payment':
            return validatePaymentForm();
        default:
            return validateForm();
    }
}

/**
 * Send a post request to server and handle it
 */
function postNewRow(table){
    let request = getRequest(table);
    if(!request){
        // Form is not valid (missing/wrong fields)
        console.log("invalid form");
        return false;
    }
    beforeModalRequest();
    let baseURL = location.protocol+'//'+location.hostname+(location.port ? ':'+location.port: '');
    let postURL = baseURL + "/api/add/";
    let xhttp = new XMLHttpRequest();
    xhttp.open("POST", postURL, true);
    xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    xhttp.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
    xhttp.onreadystatechange = function() {
        if(xhttp.readyState === 4) {
            if (xhttp.status !== 200) {
                document.getElementById("form-" + table + "-error").className = "alert alert-danger";
                if(xhttp.responseText !== ''){
                    document.getElementById("form-" + table + "-error-msg").innerHTML = xhttp.responseText;
                } else {
                    document.getElementById("form-" + table + "-error-msg").innerHTML = xhttp.status + ': ' + xhttp.statusText;
                }
            } else {
                document.getElementById("form-" + table + "-error").className = "alert alert-danger hidden"; // hide old msg
                dismissModal();
                new PNotify({
                    title: 'Succès!',
                    text: 'Élément ajouté avec succès',
                    type: 'success'
                });
                drawDataTable(table);
            }
            afterModalRequest();
        }
    };
    xhttp.send(request)
}

/**
 * Send a post request to server and handle it
 */
function postEditRow(table){
    let request = getRequest(table);
    if(!request){
        // Form is not valid (missing/wrong fields)
        return false;
    }
    beforeModalRequest();
    let baseURL = location.protocol+'//'+location.hostname+(location.port ? ':'+location.port: '');
    let postURL = baseURL + "/api/edit/?" + request;
    let xhttp = new XMLHttpRequest();
    xhttp.open("POST", postURL, true);
    xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    xhttp.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
    xhttp.onreadystatechange = function() {
        if(xhttp.readyState === 4) {
            if (xhttp.status !== 200) {
                if (xhttp.responseText) {
                    console.log("POST error on new element");
                    document.getElementById("form-" + table + "-error").className = "alert alert-danger";
                    document.getElementById("form-" + table + "-error-msg").innerHTML = xhttp.responseText;
                }
            } else {
                document.getElementById("form-" + table + "-error").className = "alert alert-danger hidden"; // hide old msg
                dismissModal();
                new PNotify({
                    title: 'Succès!',
                    text: 'Élément édité avec succès',
                    type: 'success'
                });
                drawDataTable(table);
            }
            afterModalRequest();
        }
    };
    xhttp.send(request)
}

function getDataTableFrenchTranslation(){
    return {
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
            "sFirst": '<i class="fas fa-angle-double-left fa-lg"></i>',
            "sPrevious": '<i class="fas fa-angle-left fa-lg"></i>',
            "sNext": '<i class="fas fa-angle-right fa-lg"></i>',
            "sLast": '<i class="fas fa-angle-double-right fa-lg"></i>'
        },
        "oAria": {
            "sSortAscending": ": activer pour trier la colonne par ordre croissant",
            "sSortDescending": ": activer pour trier la colonne par ordre d&eacute;croissant"
        },
        buttons: {
            pageLength: {
                _: "Afficher %d éléments <i class='fas fa-angle-down'></i>",
                '-1': "Tout afficher <i class='fas fa-angle-down'></i>"
            }
        },
    }
}

function beforeModalRequest(){
    //Disable the button to avoid multiple send and put loading spinner
    let button = $('.modal-confirm');
    button.prop('disabled', true);
    button.append('<i class="loader fas fa-spinner fa-spin"></i>');
    button.addClass('loading');
}

function afterModalRequest(){
    let button = $('.modal-confirm');
    button.prop('disabled', false);
    button.find('.loader').remove();
}

/**
 * Get the value of
 * @param cookieName a cookie
 * @returns {string} the value
 */
function getCookie(cookieName)
{
    if (document.cookie.length > 0)
    {
        let cookieStart = document.cookie.indexOf(cookieName + "=");
        if (cookieStart !== -1)
        {
            cookieStart = cookieStart + cookieName.length + 1;
            let cookieEnd = document.cookie.indexOf(";", cookieStart);
            if (cookieEnd === -1) cookieEnd = document.cookie.length;
            return unescape(document.cookie.substring(cookieStart,cookieEnd));
        }
    }
    return "";
}

/**
 * Set a new URL for a datatable, useful for live changes of DataTable URL logic
 * @param table the table name
 * @param optional additional parameters
 */
function setTableURL(table, optional){
    let baseURL = location.protocol+'//'+location.hostname+(location.port ? ':'+location.port: '');
    let dataURL = baseURL + "/api/table/?name=" + table + optional;
    $('#datatable-'+table).DataTable().ajax.url(dataURL).load();
}
