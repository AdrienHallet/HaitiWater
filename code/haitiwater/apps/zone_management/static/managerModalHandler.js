$(document).ready(function() {

    //Show only relevant form component to the desired user type
    $('#form-add-manager').find('#select-type').on('click', function(){
        $('#form-group-select-zone').addClass('hidden');
        $('#form-group-multiselect-outlets').addClass('hidden');

        if(this.value === 'fountain-manager'){
            $('#form-group-multiselect-outlets').removeClass('hidden');
        }
        else if (this.value === 'zone-manager'){
            $('#form-group-select-zone').removeClass('hidden');
        }
    });
});


/**
 * Validate (check if valid) the form.
 * If not valid, display messages
 */
function validateForm() {
    let form = document.forms["form-add-manager"];

    let id = form["input-id"].value;
    let name = form["input-name"].value;

    let missing = false;
    if (name.trim() === "") {
        document.getElementById("input-name-error").className = "error";
        missing = true;
    }

    //TODO

    if(missing){
        return false
    } else {
        return buildRequest(id, name);
    }

}

/**
 * Build the request
 * @param id
 * @param lastName
 * @param firstName
 * @param role
 * @param zone
 * @returns {string}
 */
function buildRequest(id, lastName, firstName, role, zone){
    let request = "table=manager";
    request += "&id=" + id;
    request += "&lastname=" + lastName;
    request += "&firstname=" + firstName;
    request += "&role=" + role;
    request += "&zone=" + zone;

    return request;
}

/**
 * Hide the error message in the form
 */
function hideFormErrorMsg(){
    document.getElementById("form-error").className = "alert alert-danger hidden";
}

function setupModalManagerAdd(){
    //Show add components
    $('#modal-manager-title-add').removeClass("hidden");
    $('#modal-manager-submit-add').removeClass("hidden");

    //Hide edit components
    $('#modal-manager-title-edit').addClass("hidden");
    $('#modal-manager-submit-edit').addClass("hidden");
    $('#form-manager-id-component').addClass("hidden");

    showManagerModal();
}

function setupModalManagerEdit(data){
    //Todo
}

function showManagerModal(){
    $('#plus-manager').magnificPopup({
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
