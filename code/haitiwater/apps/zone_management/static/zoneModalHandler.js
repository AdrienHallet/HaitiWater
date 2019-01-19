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
        console.log("missing zone element");
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
    //Hide add components
    $('#modal-zone-title-add').addClass("hidden");
    $('#modal-zone-submit-add').addClass("hidden");

    //Show edit components
    $('#modal-zone-title-edit').removeClass("hidden");
    $('#modal-zone-submit-edit').removeClass("hidden");
    $('#form-zone-id-component').removeClass("hidden");

    //Fill with existing data
    $('#input-zone-id').val(data[0].innerText);
    $('#input-zone-name').val(data[1].innerText);

    showZoneModal();
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
 * Hide the modal and clear the fields
 */
function dismissZoneModal() {
    $.magnificPopup.close();
    $('form').find('input').val('');
}
