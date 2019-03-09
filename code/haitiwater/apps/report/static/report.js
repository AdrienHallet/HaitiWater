$(document).ready(function() {
    if (location.pathname !== '/offline/') {
        drawTicketTable();
        drawReportTable();
    }

    $('#input-picture').on('change', function(){
        readURL(this);
    });
});
