/**
 * Validate (check if valid) the form.
 * If not valid, display messages
 */
function validateZoneForm() {
    let form = document.forms["form-add-zone"];

    let id = form["input-zone-id"].value;
    let name = form["input-zone-name"].value;

    let missing = false;
    if (name.trim() === "") {
        document.getElementById("input-zone-name-error").className = "error";
        missing = true;
    }

    if(missing){
        return false
    } else {
        return buildZoneRequest(id, name);
    }

}

/**
 * Build the request
 * @param id
 * @param name
 * @returns {string}
 */
function buildZoneRequest(id, name){
    let request = "table=zone";
    request += "&id=" + id;
    request += "&name=" + name;

    return request;
}

/**
 * Hide the error message in the form
 */
function hideFormErrorMsg(){
    document.getElementById("form-zone-error").className = "alert alert-danger hidden";
}

function setupModalZoneAdd(){
    //Show add components
    $('#modal-zone-title-add').removeClass("hidden");
    $('#modal-zone-submit-add').removeClass("hidden");

    //Hide edit components
    $('#modal-zone-title-edit').addClass("hidden");
    $('#modal-zone-submit-edit').addClass("hidden");
    $('#form-zone-id-component').addClass("hidden");

    showZoneModal();
}

function setupModalZoneEdit(data){
    //Todo
}

function showZoneModal(){
    $('#plus-zone').magnificPopup({
        type: 'inline',
        preloader: false,
        focus: '#name',
        modal: true,

        // Do not zoom on mobile
        callbacks: {
            beforeOpen: function() {
                if($(window).width() < 700) {
                    this.st.focus = false;
                } else {
                    this.st.focus = '#name';
                }
            }
        }
    }).magnificPopup('open');
}

/**
 * Hide the modal
 */
function dismissModal() {
    $.magnificPopup.close();
}
