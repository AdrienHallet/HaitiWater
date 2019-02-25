$(document).ready(function() {

});

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

    console.log(data);
    attachComputeGainsHandler();
    attachCubicGallonConverter();
}

function attachComputeGainsHandler(){
    $('.water-outlet').each(function(i){
        $('input', this).on('input', function(){
            let sum = $('.cubic input').val() * $('.per-cubic input').val();
            $('.computed-gains').val(sum);
        });
    });
}
