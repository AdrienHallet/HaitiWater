$(document).ready(function() {
    if (location.pathname !== '/offline/')
        drawTicketTable();

    $('#input-picture').on('change', function(){
        readURL(this);
    });
});
