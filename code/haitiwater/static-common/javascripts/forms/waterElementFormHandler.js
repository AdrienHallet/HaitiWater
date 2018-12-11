/**
 * Validate (check if valid) the form.
 * If not valid, display messages
 */
function validateForm() {
    let form = document.forms["form-add-element"];

    let id = form["input-id"].value;
    let type = form["select-type"].value;
    let localization = form["input-localization"].value;
    let state = form["select-state"].value;

    let missing = false;
    if (type === "none") {
        document.getElementById("select-type-error").className = "error";
        missing = true;
    }
    if (localization.trim() === "") {
        document.getElementById("input-localization-error").className = "error";
        missing = true;
    }
    if (state === "none") {
        document.getElementById("select-state-error").className = "error";
        missing = true;
    }

    if(missing){
        return false
    } else {
        return buildRequest(id, type, localization, state);
    }

}

/**
 * Build the request
 * @param id
 * @param type
 * @param localization
 * @param state
 * @returns {string}
 */
function buildRequest(id, type, localization, state){
    let request = "table=water_element";
    request += "&id=" + id;
    request += "&type=" + type;
    request += "&localization=" + localization;
    request += "&state=" + state;

    return request;
}

/**
 * Hide the error message in the form
 */
function hideFormErrorMsg(){
    document.getElementById("form-error").className = "alert alert-danger hidden";
}

function setupModalAdd(){
    //Show add components
    $('#modal-title-add').removeClass("hidden");
    $('#modal-submit-add').removeClass("hidden");

    //Hide edit components
    $('#modal-title-edit').addClass("hidden");
    $('#modal-submit-edit').addClass("hidden");
    $('#form-id-component').addClass("hidden");

    showModal();
}

function setupModalEdit(data){
    //Hide add components
    $('#modal-title-add').addClass("hidden");
    $('#modal-submit-add').addClass("hidden");

    //Show edit components
    $('#modal-title-edit').removeClass("hidden");
    $('#modal-submit-edit').removeClass("hidden");
    $('#form-id-component').removeClass("hidden");

    //Get the option that contains the values for data 2 and 4
    let typeOption = $("#select-type option").filter(function() {
        if (this.text.trim() === data[1].innerText.trim()) {
            return this;
        }
    });
    let stateOption = $("#select-state option").filter(function() {
        if (this.text.trim() === data[4].innerText.trim()) {
            return this;
        }
    });

    //Set form values to current values
    let form = document.forms["form-add-element"];
    form["input-id"].value = data[0].innerText;
    form["select-type"].value = typeOption[0].value;
    form["input-localization"].value = data[2].innerText;
    form["select-state"].value = stateOption[0].value;

    showModal();
}

function showModal(){
    $('#call-water-modal').magnificPopup({
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
 * Hide the modal and reset the fields
 */
function dismissModal() {
    $.magnificPopup.close();
    let form = document.forms["form-add-element"];
    form["select-type"].value = "none";
    form["input-localization"].value = "";
    form["select-state"].value = "none";

}
