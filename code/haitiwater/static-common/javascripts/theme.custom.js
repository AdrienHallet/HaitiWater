$( document ).ready(function() {

    //Get local storage value or true (as it is default to be open)
    let isMenuOpen = (localStorage.getItem('isMenuOpen') === 'true');
    if(!isMenuOpen){
        $('html').addClass('sidebar-left-collapsed')
    }

    //Toggle menu position on localstorage to save collapsed state
    $('.sidebar-toggle').on('click', function (){
        isMenuOpen = !isMenuOpen;
        localStorage.setItem('isMenuOpen', isMenuOpen.toString());
    })

});