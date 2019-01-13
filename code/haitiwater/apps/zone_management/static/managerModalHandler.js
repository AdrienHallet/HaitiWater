$(document).ready(function() {

    //Show only relevant form component to the desired user type
    $('#form-add-manager').find('#select-manager-type').on('click', function(){
        $('#form-group-select-zone').addClass('hidden');
        $('#form-group-multiselect-outlets').addClass('hidden');

        if(this.value === 'fountain-manager'){
            requestAvailableWaterElements();
            $('#form-group-multiselect-outlets').removeClass('hidden');
        }
        else if (this.value === 'zone-manager'){
            requestAvailableZones();
            $('#form-group-select-zone').removeClass('hidden');
        }
    });
});


function requestAvailableZones(){
    let select = $('#select-manager-zone');
    select.html("");
    let baseURL = location.protocol+'//'+location.hostname+(location.port ? ':'+location.port: '');
    let postURL = baseURL + "/api/table/?name=zone&draw=0&columns%5B0%5D%5Bdata%5D=0&columns%5B0%5D%5Bname%5D=&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=true&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=1&columns%5B1%5D%5Bname%5D=&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=true&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=&columns%5B2%5D%5Bname%5D=&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=false&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=0&order%5B0%5D%5Bdir%5D=asc&start=0&length=-1&search%5Bvalue%5D=&search%5Bregex%5D=false";
    var xhr = new XMLHttpRequest();
    xhr.open('GET', postURL, true);
    xhr.responseType = 'json';
    xhr.onload = function() {
      var status = xhr.status;
      if (status === 200) {
        let zones = xhr.response.data;
        zones.forEach(function(zone){
            select.append(
                '<option value="' + zone[0] + '">' + zone[1] + '</option>'
            )
        });
      } else {
        console.log(xhr.response);
      }
    };
    xhr.send();
}


function requestAvailableWaterElements(){
    let multiselect = $('#multiselect-manager-outlets');
    multiselect.html("");
    let baseURL = location.protocol+'//'+location.hostname+(location.port ? ':'+location.port: '');
    let postURL = baseURL + "/api/table/?name=water_element&draw=0&columns%5B0%5D%5Bdata%5D=0&columns%5B0%5D%5Bname%5D=&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=true&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=1&columns%5B1%5D%5Bname%5D=&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=true&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=2&columns%5B2%5D%5Bname%5D=&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=true&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=3&columns%5B3%5D%5Bname%5D=&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable%5D=true&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=4&columns%5B4%5D%5Bname%5D=&columns%5B4%5D%5Bsearchable%5D=true&columns%5B4%5D%5Borderable%5D=true&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B5%5D%5Bdata%5D=5&columns%5B5%5D%5Bname%5D=&columns%5B5%5D%5Bsearchable%5D=true&columns%5B5%5D%5Borderable%5D=true&columns%5B5%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B5%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B6%5D%5Bdata%5D=6&columns%5B6%5D%5Bname%5D=&columns%5B6%5D%5Bsearchable%5D=true&columns%5B6%5D%5Borderable%5D=true&columns%5B6%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B6%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B7%5D%5Bdata%5D=7&columns%5B7%5D%5Bname%5D=&columns%5B7%5D%5Bsearchable%5D=true&columns%5B7%5D%5Borderable%5D=true&columns%5B7%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B7%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B8%5D%5Bdata%5D=&columns%5B8%5D%5Bname%5D=&columns%5B8%5D%5Bsearchable%5D=true&columns%5B8%5D%5Borderable%5D=false&columns%5B8%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B8%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=0&order%5B0%5D%5Bdir%5D=asc&start=0&length=-1&search%5Bvalue%5D=&search%5Bregex%5D=false";
    var xhr = new XMLHttpRequest();
    xhr.open('GET', postURL, true);
    xhr.responseType = 'json';
    xhr.onload = function() {
      var status = xhr.status;
      if (status === 200) {
        let zones = xhr.response.data;
        zones.forEach(function(zone){
            multiselect.append(
                '<option value="' + zone[0] + '">' + zone[1] + " " + zone[2] + '</option>'
            )
        });
      } else {
        console.log(xhr.response);
      }
    };
    xhr.send();
}

/**
 * Check the validity of an email
 * @param email the email to test
 * @returns {*|boolean} true if email is a valid email address
 */
function validateEmail(email) {
    var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase());
}

/**
 * Validate (check if valid) the form.
 * If not valid, display messages
 */
function validateManagerForm() {
    console.log("validating");
    let form = document.forms["form-add-manager"];

    let id = form["input-manager-id"].value;
    let lastName = form["input-manager-last-name"].value;
    let firstName = form["input-manager-first-name"].value;
    let email = form["input-manager-email"].value;
    let type = form["select-manager-type"].value;
    let zone = form["select-manager-zone"].value;

    let outlets = $('#multiselect-manager-outlets').val();


    // Construct an object with selectors for the fields as keys, and
    // per-field validation functions as values like so
    const fieldsToValidate = {
      '#input-manager-last-name' : value => value.trim() !== '',
      '#input-manager-first-name' : value => value.trim() !== '',
      '#input-manager-id' : value => value.trim() !== '',
      '#input-manager-email' : value => validateEmail(value),
      '#select-manager-type' : value => value.trim() !== 'none',
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

    if (type === 'fountain-manager'){
        if (outlets == null){
            console.log('no fountain');
            $('#multiselect-manager-outlets-error').removeClass('hidden');
            return false;
        }
    }
    if (type === 'zone-manager'){
        if (zone === 'none'){
            console.log('no zone');
            $('#select-manager-zone-error').removeClass('hidden');
            return false;
        }
    }

    // If invalid field length is greater than zero, this signifies
    // a form state that failed validation
    if(invalidFields.length > 0){
        console.log('invalid');
        return false
    } else {
        return buildManagerRequest(id,
            lastName,
            firstName,
            email,
            type,
            zone,
            outlets);
    }

}

function buildManagerRequest(id, lastName, firstName, email, type, zone, outlets){
    let request = "table=manager";
    request += "&id=" + id;
    request += "&lastname=" + lastName;
    request += "&firstname=" + firstName;
    request += "&email=" + email;
    request += "&type=" + type;
    request += "&zone=" + zone;
    request += "&outlets=" + outlets;

    return request;
}

function setupModalManagerAdd(){
    //Show add components
    $('#modal-manager-title-add').removeClass("hidden");
    $('#modal-manager-submit-add').removeClass("hidden");

    //Hide edit components
    $('#modal-manager-title-edit').addClass("hidden");
    $('#modal-manager-submit-edit').addClass("hidden");

    //Enable personal information modification
    disableModalElements(false);

    showManagerModal();
}

function disableModalElements(bool){
    $('#input-manager-id').prop('disabled', bool);
    $('#input-manager-first-name').prop('disabled', bool);
    $('#input-manager-last-name').prop('disabled', bool);
    $('#input-manager-email').prop('disabled', bool);
}

function setupModalManagerEdit(data){
    //Show add components
    $('#modal-manager-title-add').addClass("hidden");
    $('#modal-manager-submit-add').addClass("hidden");

    //Hide edit components
    $('#modal-manager-title-edit').removeClass("hidden");
    $('#modal-manager-submit-edit').removeClass("hidden");

    //Disable the modification of personal information
    disableModalElements(true);

    //Setup elements
    $('#input-manager-id').val(data[0].innerText);
    $('#input-manager-last-name').val(data[1].innerText);
    $('#input-manager-first-name').val(data[2].innerText);
    $('#input-manager-email').val(data[3].innerText);
    $('#select-manager-type').val(data[4].innerText);

    showManagerModal();
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
 * Hide the modal and empty the values
 */
function dismissManagerModal() {
    $.magnificPopup.close();
    $('form').find('input').val('');
}
