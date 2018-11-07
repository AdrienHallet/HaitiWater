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

/**
 * Validate (check if valid) the form.
 * If not valid, display messages
 * @returns {boolean}
 */
function validateForm() {
    console.log("Form validation start");

    let form = document.forms["form-add-element"];

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
        let request = buildRequest(type, localization, state);
        postNewElement(request);
    }

}

/**
 * Build the request
 * @param type
 * @param localization
 * @returns {string}
 */
function buildRequest(type, localization, state){
    let request = "table=water_element";
    request += "&type=" + type;
    request += "&localization=" + localization;
    request += "&state=" + state;

    return request;
}

/**
 * Send a post request to server and handle it
 * @param request as a String
 * //Todo extract
 */
function postNewElement(request){
    let baseURL = location.protocol+'//'+location.hostname+(location.port ? ':'+location.port: '');
    let postURL = baseURL + "/api/add/";
    let xhttp = new XMLHttpRequest();
    xhttp.open("POST", postURL, true);
    xhttp.onreadystatechange = function() {
        if(xhttp.readyState !== 4 || xhttp.status !== 200) {
            if(xhttp.responseText) {
                console.log("POST error on new element");
                document.getElementById("form-error").className = "alert alert-danger";
                document.getElementById("form-error-msg").innerHTML = xhttp.responseText;
            }
        } else {
            dismissModal();
            new PNotify({
                title: 'Succès!',
                text: 'Élément ajouté avec succès',
                type: 'success'
            });
        }
    };
    xhttp.send(request)
}

/**
 * Hide the error message in the form
 */
function hideFormErrorMsg(){
    document.getElementById("form-error").className = "alert alert-danger hidden";
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
