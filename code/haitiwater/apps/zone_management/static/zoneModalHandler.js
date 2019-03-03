/**
 * Validate (check if valid) the form.
 * If not valid, display messages
 */
function validateZoneForm() {
    let form = document.forms["form-add-zone"];

    let id = form["input-zone-id"].value;
    let name = form["input-zone-name"].value;
    let outletPrice = form["input-outlet-price-value"].value;
    let outletDuration = form["select-outlet-price-duration"].value;

    let valid = true;
    if (name.trim() === "") {
        document.getElementById("input-zone-name-error").className = "error";
        valid = false;
    }
    if (outletPrice < 0){
        $('#form-zone-error-msg').html("Vous ne pouvez entrer un coût négaif");
        $('#form-zone-error').removeClass('hidden');
        valid = false;
    }

    if(valid){
        return buildZoneRequest(id, name, outletPrice, outletDuration);
    }
    return false;

}

/**
 * Build the request
 * @param id id of the zone (if edition, empty otherwise)
 * @param name of the zone
 * @param outletPrice price for non-individuals outlets
 * @param outletDuration duration of the bill for non-individuals outlets
 * @returns {string} the request
 */
function buildZoneRequest(id, name, outletPrice, outletDuration){
    let request = "table=zone";
    request += "&id=" + id;
    request += "&name=" + name;
    request += "&outlet-price=" + outletPrice;
    request += "&outlet-duration=" + outletDuration;

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
    $('form').find('select').val(1);
}
