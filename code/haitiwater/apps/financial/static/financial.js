let paymentTable = 'undefined';

$(document).ready(function() {
    // Draw DataTables
    let zoneTable = drawZoneTable();
    let consumerTable = drawConsumerTable(false);

    attachHandlers(zoneTable, consumerTable);
});

/**
 * Attach the handlers for onclick navigation
 * @param zoneTable to attach event to
 * @param consumerTable to attach event to
 */
function attachHandlers(zoneTable, consumerTable){
    $('#datatable-consumer').first('tbody').on('click', 'tr td:not(:last-child)', function(){
        $('#consumer-payment-details').removeClass('hidden');
        consumerDetails(consumerTable.row($(this).closest('tr')).data());
    });

    $('#datatable-zone').first('tbody').on('click', 'tr td:not(:last-child)', function(){
        let row = ($(this).closest('tr'));
        filterConsumersFromZone(zoneTable);
    });
}

/**
 * Automatically fill the field on the manager table from the selected zone
 * (Takes the data from the first tr.selected)
 *
 * @param zoneTable the table zone datatable object
 */
function filterConsumersFromZone(zoneTable){
    let data = zoneTable.row('tr.selected').data();
    let consumerTable = $('#datatable-consumer').DataTable();
    if  (data == null){ // If nothing selected
        consumerTable.search("").draw();
        return;
    }
    let zoneName = data[1];
    consumerTable.search(zoneName).draw();

}

/**
 * Setup the consumer details window
 * @param data the datatable row
 */
function consumerDetails(data){
    let userID = data[0];
    if (paymentTable === 'undefined') {
        paymentTable = drawPaymentTable();
    }
    setTableURL('payment', '&user=' + userID);
    drawDataTable('payment');
    $('#input-payment-id-consumer').val(userID);

    let userName = data[1] + " " + data[2];
    $('.consumer-name-details').html(userName);

    requestFinancialDetails(userID);

    $('#consumer-details-id').html(data[0]);
    $('#consumer-details-lastname').html(data[1]);
    $('#consumer-details-firstname').html(data[2]);
    $('#consumer-details-gender').html(data[3]);
    $('#consumer-details-address').html(data[4]);
    $('#consumer-details-phone').html(data[5]);
    $('#consumer-details-subconsumers').html(data[6]);
    $('#consumer-details-outlet').html(data[7]);
}

/**
 * Ask the server for financial details on a given user
 * @param userID the user ID
 * @return {object} the data
 */
function requestFinancialDetails(userID){
    let requestURL = "../api/details?table=payment&id=" + userID;
    let xhttp = new XMLHttpRequest();

    xhttp.onreadystatechange = function(){
        if (this.readyState === 4) {
            if (this.status === 200) {
                let financialDetails = JSON.parse(this.response);
                $('#consumer-details-amount-due').html('(HTG) ' + financialDetails.amount_due);
                $('#consumer-details-next-bill').html(financialDetails.validity);
            }
            else{
                console.log(this);
                new PNotify({
                    title: 'Échec du téléchargement',
                    text: "Impossible de récupérer les détails financiers de l'utilisateur.",
                    type: 'warning'
                })
            }
        }
    };

    xhttp.open('GET', requestURL, true);
    xhttp.send();
}

function refreshFinancialDetails() {
    requestFinancialDetails($('#input-payment-id-consumer').val());
}
