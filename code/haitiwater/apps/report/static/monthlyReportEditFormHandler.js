let formError;
let formErrorMsg;

$(document).ready(function() {
    // Init jQuery selectors
    formError = $('#form-monthly-report-edit-error');
    formErrorMsg = $('#form-monthly-report-edit-error-msg');
});
/**
 * Try to send the current report, with validation first
 */
function postReportEdit(){
    let report = getEditedData();
    if(!validateReport(report)) {
        return;
    }
    beforeModalRequest();
    let baseURL = location.protocol+'//'+location.hostname+(location.port ? ':'+location.port: '');
    let postURL = baseURL + "/api/edit/?table=report";
    let xhttp = new XMLHttpRequest();
    xhttp.open("POST", postURL, true);
    xhttp.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
    xhttp.setRequestHeader('Content-type', 'application/json');
    xhttp.onreadystatechange = function() {
        if(xhttp.readyState === 4) {
            if (xhttp.status !== 200) {
                new PNotify({
                    title: 'Échec!',
                    text: "Le rapport mensuel n'a pas pu être édité",
                    type: 'error'
                });
                formErrorMsg.html(xhttp.responseText);
                formError.removeClass('hidden');
            } else {
                new PNotify({
                    title: 'Succès!',
                    text: 'Le rapport mensuel a été édité !',
                    type: 'success'
                });
                dismissModal();
            }
            afterModalRequest()
        }
    };
    console.log(JSON.stringify(report));
    xhttp.send(JSON.stringify(report));
}

/**
 * Validates a monthly report edit form
 * @param data the report
 * @returns {boolean} true if the report is valid, false otherwise
 */
function validateReport(data){
    for(let i = 0; i < data.details.length; i++){
        let current = data.details[i];
        if (!current.has_data) continue; //Skip validation if we don't have data to validate

        if(current.volume < 0 || current.price < 0 || current.revenue < 0){
            console.log('Negative value');
            formErrorMsg.html('Les valeurs négatives ne sont pas acceptées.');
            formError.removeClass('hidden');
            return false;
        } else if(isNaN(current.volume) || isNaN(current.price) || isNaN(current.revenue) ||
                    current.volume.length <= 0 || current.price.length <= 0 || current.revenue.length <= 0){
            console.log('NaN value');
            formErrorMsg.html('Seules les valeurs numériques positives sont acceptées');
            formError.removeClass('hidden');
        } else {
            formError.addClass('hidden');
            return true;
        }
    }
}

function getEditedData(){

    let report =
        {
            id: $('#monthly-edit-id').val(),
            date: $('#monthly-edit-date').html(),
            details: [],
        };

    let sections = $('.water-outlet');
    sections.each(function(){
        let detail = {};
        detail.id = $('.outlet-id', $(this)).val();
        detail.name = $('.panel-title', $(this)).html();
        detail.has_data = $('.element-activity', $(this)).is(':checked');
        detail.volume = $('.cubic input', $(this)).val();
        detail.price = $('.per-cubic input', $(this)).val();
        detail.revenue = $('.real-gains input', $(this)).val();
        report.details.push(detail);
    });

    return report;
}

/**
 * Hide the modal and reset the fields
 */
function dismissModalMonthlyReportEdit() {
    $.magnificPopup.close();
}

/**
 * Setup and shows the modal
 * @param data the report data
 */
function setupModalMonthlyReportEdit(data){
    $('#monthly-edit-date').html(data.date);
    $('#monthly-edit-id').val(data.id);

    cloneWaterOutletSection(data.details.length);
    attachComputeGainsHandler();
    attachCubicGallonConverter();
    fillExistingData(data.details);
    attachNumericInputHandler();
}

/**
 * Clone the water element section n times
 * @param n
 */
function cloneWaterOutletSection(n){
    let waterOutletHTML = document.getElementsByClassName('water-outlet');
    // Remove old outlets, keep one (index 0) as the model
    while(waterOutletHTML[1]){
        waterOutletHTML[1].remove();
    }
    // Add n-1 new clones
    for(let i = 1; i < n; i++){
        let copy = waterOutletHTML[0].cloneNode(true);
        waterOutletHTML[0].parentNode.insertBefore(copy, waterOutletHTML[0]);
    }
}

/**
 * Fill the water elements input
 * @param data the data in the monthly report
 */
function fillExistingData(data){
    let sections = $('.water-outlet');
    if(data.length !== sections.length){
        console.log("Error parsing the data");
        new PNotify({
            title: 'Échec!',
            text: "L'édition est impossible en raison d'une erreur interne",
            type: 'failure'
        });
        return;
    }
    sections.each(function(index){
        let detail = data[index];
        $('.outlet-id', $(this)).val(detail.id);
        $('.panel-title', $(this)).html(detail.name);
        $('.cubic input', $(this)).val(detail.volume).trigger('input');
        $('.per-cubic input', $(this)).val(detail.price).trigger('input');
        $('.real-gains input', $(this)).val(detail.revenue);
    });
}

/**
 * Attach a listener that computes the value for the gains (volume * price per volume)
 */
function attachComputeGainsHandler(){
    $('.water-outlet').each(function(i){
        $('input', this).on('input', function(){
            let sum = $('.cubic input').val() * $('.per-cubic input').val();
            $('.computed-gains').val(sum);
        });
    });
}