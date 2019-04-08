/**
 * Validate (check if valid) the form.
 * If not valid, display messages
 */
function validateZoneForm() {
    let form = document.forms["form-add-zone"];

    let id = form["input-zone-id"].value;
    let name = form["input-zone-name"].value;
    let fountainPrice = form["input-fountain-price-value"].value;
    let fountainDuration = form["select-fountain-price-duration"].value;
    let kioskPrice = form["input-kiosk-price-value"].value;
    let kioskDuration = form["select-kiosk-price-duration"].value;
    let indivPrice = form["input-indiv-price-value"].value;
    let indivDuration = form["select-indiv-price-duration"].value;

    let valid = true;
    if (name.trim() === "") {
        document.getElementById("input-zone-name-error").className = "error";
        valid = false;
    }
    console.log(fountainPrice);
    if (fountainPrice < 0 || kioskPrice < 0){
        $('#form-zone-error-msg').html("Vous ne pouvez entrer un coût négaif");
        $('#form-zone-error').removeClass('hidden');
        valid = false;
    }
    if (fountainPrice === ""){
        fountainPrice = 0
    }
    if (kioskPrice === ""){
        kioskPrice = 0
    }
    if (indivPrice === ""){
        indivPrice = 0
    }
    if(valid){
        return buildZoneRequest(
            id,
            name,
            fountainPrice,
            fountainDuration,
            kioskPrice,
            kioskDuration,
            indivPrice,
            indivDuration
        );
    }
    return false;

}

/**
 * Build the request
 * @param id id of the zone (if edition, empty otherwise)
 * @param name of the zone
 * @param fountainPrice price for fountains
 * @param fountainDuration duration of the bill for fountains
 * @param kioskPrice price for kiosks
 * @param kioskDuration duration of the bill for kiosks
 * @param indivPrice price for individual outlets
 * @param indivDuration duration of the bill for individual outlets
 * @returns {string} the request
 */
function buildZoneRequest(id, name, fountainPrice, fountainDuration, kioskPrice, kioskDuration, indivPrice, indivDuration){
    let request = "table=zone";
    request += "&id=" + id;
    request += "&name=" + name;
    request += "&fountain-price=" + fountainPrice;
    request += "&fountain-duration=" + fountainDuration;
    request += "&kiosk-price=" + kioskPrice;
    request += "&kiosk-duration=" + kioskDuration;
    request += "&indiv-price=" + indivPrice;
    request += "&indiv-duration=" + indivDuration;

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

    //Empty inputs
    $('#input-zone-id').val("");
    $('#input-zone-name').val("");

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
    $('#input-zone-id').val(data[0]);
    $('#input-zone-name').val(data[1]);

    $('#input-fountain-price-value').val(data[2]);
    $('#select-fountain-price-duration').val(data[3]);

    $('#input-kiosk-price-value').val(data[4]);
    $('#select-kiosk-price-duration').val(data[5]);

    $('#input-indiv-price-value').val(data[6]);
    $('#select-indiv-price-duration').val(data[7]);

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
