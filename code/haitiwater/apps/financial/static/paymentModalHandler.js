/**
 * Validate (check if valid) the form.
 * If not valid, display messages
 */
function validatePaymentForm() {
    let form = document.forms["form-add-payment"];

    let id = form["input-payment-id"].value;
    let amount = form["input-payment-value"].value;

    if (amount <= 0) {
        $("#input-payment-value-error").removeClass('hidden');
        return false;
    }
    return buildPaymentRequest(id, amount);

}

function buildPaymentRequest(id, amount){
    let request = "table=payment";
    request += "&id=" + id;
    request += "&amount=" + amount;

    return request;
}

function setupModalPaymentAdd(){
    //Show add components
    $('#modal-payment-title-add').removeClass("hidden");
    $('#modal-payment-submit-edit').removeClass("hidden");

    //Hide edit components
    $('#modal-payment-title-edit').addClass("hidden");
    $('#modal-payment-submit-edit').addClass("hidden");

    showPaymentModal();
}

function setupModalPaymentEdit(data){
    //Show add components
    $('#modal-payment-title-add').addClass("hidden");
    $('#modal-payment-submit-add').addClass("hidden");

    //Hide edit components
    $('#modal-payment-title-edit').removeClass("hidden");
    $('#modal-payment-submit-edit').removeClass("hidden");

    //Setup elements
    $('#input-payment-id').val(data[0]);
    $('#input-payment-value').val(data[1]);

    showPaymentModal();
}

function showPaymentModal(){
    $('#call-payment-modal').magnificPopup({
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
function dismissPaymentModal() {
    $.magnificPopup.close();
    $('form').find('input').val('');
}
