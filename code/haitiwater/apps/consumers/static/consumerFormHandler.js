function validateForm() {
    let form = document.forms["form-add-consumer"];

    let id = form["input-id"].value;
    let lastName = form["input-last-name"].value;
    let firstName = form["input-first-name"].value;
    let gender = form["select-gender"].value;
    let address = form["input-address"].value;
    let phone = form["input-phone"].value;
    let subConsumers = form["input-sub-consumers"].value;
    let mainOutlet = form["select-main-outlet"].value;


    // Construct an object with selectors for the fields as keys, and
    // per-field validation functions as values like so
    const fieldsToValidate = {
      '#input-last-name' : value => value.trim() !== '',
      '#input-first-name' : value => value.trim() !== '',
      '#select-gender' : value => value !== 'none',
      '#input-address' : value => value.trim() !== '',
      '#input-phone' : value => (value === '' || value.toString().length === 8), // Haiti has 8 digits phone numbers
      '#select-main-outlet' : value => value !== 'none',
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
    if(invalidFields.length > 0){
        return false
    } else {
        return buildRequest(id,
            lastName,
            firstName,
            gender,
            address,
            Math.abs(phone),
            Math.abs(subConsumers),
            mainOutlet);
    }
}

function buildRequest(id, lastName, firstName, gender, address, phone, subConsumers, mainOutlet){
    let request = "table=consumer";
    request += "&id=" + id;
    request += "&lastname=" + lastName;
    request += "&firstname=" + firstName;
    request += "&gender=" + gender;
    request += "&address=" + address;
    request += "&phone=" + phone; // Nullable
    request += "&subconsumer=" + subConsumers; // Nullable
    request += "&mainOutlet=" + mainOutlet;

    return request;
}

function setupModalConsumerAdd(){
    //Show add components
    $('#modal-title-add').removeClass("hidden");
    $('#modal-submit-add').removeClass("hidden");

    //Hide edit components
    $('#modal-title-edit').addClass("hidden");
    $('#modal-submit-edit').addClass("hidden");
    $('#form-id-component').addClass("hidden");

    showModalConsumer();
}

function setupModalConsumerEdit(data){
    //Show add components
    $('#modal-title-add').addClass("hidden");
    $('#modal-submit-add').addClass("hidden");

    //Hide edit components
    $('#modal-title-edit').removeClass("hidden");
    $('#modal-submit-edit').removeClass("hidden");
    $('#form-id-component').removeClass("hidden");

    //Fill the form with existing data
    let form = document.forms['form-add-consumer'];
    form['input-id'].value = data[0];
    form['input-last-name'].value = data[1];
    form['input-first-name'].value = data[2];

     //Get the option that contains the values for data 2 and 4
    let genderOption = $("#select-gender option").filter(function() {
        if (this.text.trim() === data[3].trim()) {
            return this;
        }
    });
    form['select-gender'].value = genderOption[0].value;

    form['input-address'].value = data[4];
    let currentPhone = data[5];
    console.log(currentPhone);
    if(currentPhone !== '0' && currentPhone !== "")
        form['input-phone'].value = currentPhone;
    form['input-sub-consumers'].value = data[6];

     //Get the option that contains the values for data 2 and 4
    let mainOutlet = $("#select-main-outlet option").filter(function() {
        if (this.text.trim() === data[7].trim()) {
            return this;
        }
    });
    if(mainOutlet[0] != null)
        form['select-main-outlet'].value = mainOutlet[0].value;

    showModalConsumer();
}

function showModalConsumer(){
    $('#call-consumer-modal').magnificPopup({
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
    let form = document.forms["form-add-consumer"];

    form["input-last-name"].value = "";
    form["input-first-name"].value = "";
    form["select-gender"].value = "none";
    form["input-address"].value = "";
    form["input-phone"].value = "";
    form["input-sub-consumers"].value = "";
    form["select-main-outlet"].value = "none";

}
