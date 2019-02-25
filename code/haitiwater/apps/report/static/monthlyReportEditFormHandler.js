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
    cloneWaterOutletSection(data.details.length);
    attachComputeGainsHandler();
    attachCubicGallonConverter();
    fillExistingData(data.details);
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
