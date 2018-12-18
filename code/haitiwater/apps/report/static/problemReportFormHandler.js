function validateForm() {
    let form = document.forms["form-add-ticket"];

    let id = form["input-id"].value;
    let type = form["select-type"].value;
    let urgency = form["select-urgency"].value;
    let comment = form["input-comment"].value;
    try{
        let reader = new FileReader();
        let picture = reader.readAsText(form["input-picture"].files[0]);
    }catch (ignored){
        //Continue
    }


    // Construct an object with selectors for the fields as keys, and
    // per-field validation functions as values like so
    const fieldsToValidate = {
      '#select-type' : value => value.trim() !== 'none',
      '#select-urgency' : value => value !== 'none',
      '#input-comment' : value => value.trim() !== '',
    };

    const invalidFields = Object.entries(fieldsToValidate)
    .filter(entry => {
        // Extract field selector and validator for this field
        const fieldSelector = entry[0];
        const fieldValueValidator = entry[1];
        const field = form.querySelector(fieldSelector);

        if(!fieldValueValidator(field.value)) {
            // For invalid field, apply the error class
            let fieldErrorSelector = '#' + field.id + '-error';
            form.querySelector(fieldErrorSelector).className = 'error';
            return true;
        }

        return false;
    });

    // If invalid field length is greater than zero, this signifies
    // a form state that failed validation
    return invalidFields.length < 1
}

function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
          $('#preview')
            .attr('src', e.target.result)
            .width(200);
        };
        reader.readAsDataURL(input.files[0]);
    }
}

function buildRequest(id, type, urgency, comment, picture){
    let request = "table=ticket";
    request += "&id=" + id;
    request += "&type=" + type;
    request += "&urgency=" + urgency;
    request += "&comment=" + comment;
    request += "&picture=" + picture;

    return request;
}

function setupTicketModalAdd(){
    //Show add components
    $('#modal-title-add').removeClass("hidden");
    $('#modal-submit-add').removeClass("hidden");

    //Hide edit components
    $('#modal-title-edit').addClass("hidden");
    $('#modal-submit-edit').addClass("hidden");
    $('#form-id-component').addClass("hidden");

    showModal('#show-ticket-modal');
}

function setupTicketModalEdit(data){
    //Show add components
    $('#modal-title-add').addClass("hidden");
    $('#modal-submit-add').addClass("hidden");

    //Hide edit components
    $('#modal-title-edit').removeClass("hidden");
    $('#modal-submit-edit').removeClass("hidden");
    $('#form-id-component').removeClass("hidden");

    showModal('#show-ticket-modal');
}

/**
 * Hide the modal and reset the fields
 */
function dismissModal() {
    $.magnificPopup.close();
    let form = document.forms["form-add-ticket"];

    form["input-id"].value = "";
    form["input-type"].value = "none";
    form["select-urgency"].value = "none";
    form["input-comment"].value = "";
    form["input-picture"].value = "";
}

function sendTicket() {
    if (!validateForm())
        return;
    let form = document.forms["form-add-ticket"];

    var formData = new FormData();
    formData.append("table", "ticket");
    formData.append("id", form["input-id"].value);
    formData.append("type", form["select-type"].value);
    formData.append("urgency", form["select-urgency"].value);
    formData.append("comment", form["input-comment"].value);
    formData.append("picture", form["input-picture"].files[0]);

    let baseURL = location.protocol+'//'+location.hostname+(location.port ? ':'+location.port: '');
    let postURL = baseURL + "/api/add/";
    $.ajax({
       url: postURL,
       type: "POST",
       data: formData,
       processData: false,
       contentType: false,
       success: function(response) {
           document.getElementById("form-ticket-error").className = "alert alert-danger hidden"; // hide old msg
           dismissModal();
           new PNotify({
               title: 'Succès!',
               text: 'Ticket ajouté avec succès',
               type: 'success'
           });
           drawDataTable(table);
       },
       error: function(jqXHR, textStatus, errorMessage) {
           document.getElementById("form-ticket-error").className = "alert alert-danger";
           document.getElementById("form-ticket-error-msg").innerHTML = textStatus + ': ' + errorMessage;
       }
    });
}
