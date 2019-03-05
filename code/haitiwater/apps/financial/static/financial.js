$(document).ready(function() {
    // Draw DataTables
    drawZoneTable();
    let consumerTable = drawConsumerTable(false);
    drawPaymentTable();

    attachHandlers(consumerTable);
});

/**
 * Attach the handlers for onclick navigation
 * @param consumerTable to attach event to
 */
function attachHandlers(consumerTable){
    $('#datatable-consumer').first('tbody').on('click', 'tr td:not(:last-child)', function(){
        consumerDetails(consumerTable.row($(this).closest('tr')).data());
    });
}

/**
 * Setup the consumer details window
 * @param data the datatable row
 */
function consumerDetails(data){
    let userID = data[0];
    setPaymentTableURL(userID);

    let userName = data[1] + " " + data[2];
    $('.consumer-name-details').html(userName);

    let financialDetails = requestFinancialDetails(userID);

    console.log(financialDetails);

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
        if (this.status === 200) {
            return JSON.parse(this.response);
        }
        else if (this.readyState === 4){
            console.log(this);
            new PNotify({
                title: 'Échec du téléchargement',
                text: "Impossible de récupérer les détails financiers de l'utilisateur.",
                type: 'warning'
            })
        }
    };

    xhttp.open('GET', requestURL, true);
    xhttp.send();
}
