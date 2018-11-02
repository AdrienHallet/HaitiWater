/**
 * Custom Table Handler
 * Used to prettify the table and make it respond to custom input and commands
 *
 */


// Let the search be executed when the user presses enter in the search field
let input = document.getElementById("submit-search");
input.addEventListener("keyup", function(event) {
  // Cancel the default action, if needed
  event.preventDefault();
  // Number 13 is the "Enter" key on the keyboard
  if (event.keyCode === 13) {
    // Trigger the button element with a click
    document.getElementById("myBtn").click();
  }
});

// Post on submit
$('#post-form').on('submit', function(event){
    event.preventDefault();
    console.log("form submitted!")  // sanity check
    create_post();
});

// Panels
(function( $ ) {

	$(function() {
		$('.panel')
			.on( 'click', '.panel-actions a.fa-plus', function( e ) {
				e.preventDefault();

				var $this,
					$panel;

				$this = $( this );
				$panel = $this.closest( '.panel' );

				$this
					.removeClass( 'fa-caret-up' )
					.addClass( 'fa-caret-down' );

				$panel.find('.panel-body, .panel-footer').slideDown( 200 );
			})
	});

})( jQuery );