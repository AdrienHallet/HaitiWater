$(document).ready(function() {
   attachNumericInputHandler();
});

function showModal(id){
    $(id).magnificPopup({
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
 * Refuse non-numeric inputs in number fields. Default on chrome but necessary on others.
 */
function attachNumericInputHandler(){
    $('input[type="number"]').keypress(function(e) {
        let a = [];
        let k = e.which;

        for (let i = 48; i < 58; i++)
            a.push(i);

        if (!(a.indexOf(k)>=0))
            e.preventDefault();
    });
}

/**
 * Pads a phone number with leading zeros
 */
 function padPhone(number){
     if (number.length === 7 || number.length === 9){
         return "0"+number;
     }
     return number;
 }
