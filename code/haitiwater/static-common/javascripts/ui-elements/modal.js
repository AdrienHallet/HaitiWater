// Open modal with a form
$('.modal-with-form').magnificPopup({
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
});

// Dismiss modal
$(document).on('click', '.modal-dismiss', function (e) {
    e.preventDefault();
    $.magnificPopup.close();
});

// Confirm modal
$(document).on('click', '.modal-confirm', function (e) {
    e.preventDefault();
    $.magnificPopup.close();

    new PNotify({
        title: 'Success!',
        text: 'Modal Confirm Message.',
        type: 'success'
    });
});