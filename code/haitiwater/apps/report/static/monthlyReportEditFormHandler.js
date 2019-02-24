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
    showModal('#button-modal-edit-report');
    $('#monthly-edit-date').html(data.date);

    attachCubicGallonConverter();
}