$(document).ready(function() {

    /*
	Wizard Controller
	*/
	let $wizardMonthlyReportfinish = $('#wizardMonthlyReport').find('ul.pager li.finish');

	$wizardMonthlyReportfinish.on('click', function( ev ) {
		ev.preventDefault();
		var validated = $('#wizardMonthlyReport form').valid();
		if ( validated ) {
			new PNotify({
				title: 'Congratulations',
				text: 'You completed the wizard form.',
				type: 'custom',
				addclass: 'notification-success',
				icon: 'fa fa-check'
			});
		}
	});

	$('#wizardMonthlyReport').bootstrapWizard({
		tabClass: 'wizard-steps',
		nextSelector: 'ul.pager li.next',
		previousSelector: 'ul.pager li.previous',
		firstSelector: null,
		lastSelector: null,
		onNext: function( tab, navigation, index, newindex ) {
			var validated = true; //Todo validate current form window
			if( !validated ) {
				$wizardMonthlyReportvalidator.focusInvalid();
				return false;
			}
		},
		onTabClick: function( tab, navigation, index, newindex ) {
			if ( newindex === index + 1 ) {
				return this.onNext( tab, navigation, index, newindex);
			} else return newindex <= index + 1;
		},
		onTabChange: function( tab, navigation, index, newindex ) {
			var $total = navigation.find('li').size() - 1;
			$wizardMonthlyReportfinish[ newindex !== $total ? 'addClass' : 'removeClass' ]( 'hidden' );
			$('#wizardMonthlyReport').find(this.nextSelector)[ newindex === $total ? 'addClass' : 'removeClass' ]( 'hidden' );
		},
		onTabShow: function( tab, navigation, index ) {
			var $total = navigation.find('li').length - 1;
			var $current = index;
			var $percent = Math.floor(( $current / $total ) * 100);
			$('#wizardMonthlyReport').find('.progress-indicator').css({ 'width': $percent + '%' });
			tab.prevAll().addClass('completed');
			tab.nextAll().removeClass('completed');
		}
	});


    $('#multiselect-outlets').multiselect({
        maxHeight: 300,
        buttonText: function(options, select) {
            // Note that &#9660 = caret down
            if (options.length === 0) {
                return '0 sélectionné &#9660;';
            }
            else if (options.length === 1) {
                return '1 sélectionné &#9660';
            }
            else if (options.length > 1) {
                return options.length + ' sélectionnés &#9660';
            }
        }
    });

    /*
	Multi Select: Toggle All Button
	*/
	function multiselect_selected($el) {
		var ret = true;
		$('option', $el).each(function(element) {
			if (!!!$(this).prop('selected')) {
				ret = false;
			}
		});
		return ret;
	}

	function multiselect_selectAll($el) {
		$('option', $el).each(function(element) {
			$el.multiselect('select', $(this).val());
		});
	}

	function multiselect_deselectAll($el) {
		$('option', $el).each(function(element) {
			$el.multiselect('deselect', $(this).val());
		});
	}

	function multiselect_toggle($el, $btn) {
		if (multiselect_selected($el)) {
			multiselect_deselectAll($el);
			$btn.text("Tout sélectionner");
		}
		else {
			multiselect_selectAll($el);
			$btn.text("Remise à zéro");
		}
	}

	$("#multiselect-outlets-toggle").click(function(e) {
		e.preventDefault();
		multiselect_toggle($("#multiselect-outlets"), $(this));
	});

    /**
     * Listener to convert cubic to gallons and vice-versa
     */
    $('.water-outlet').each(function(i){
        const CUBICMETER_GALLON_RATIO = 264.172;

        let cubic = $('.cubic input', this);
        let gallon = $('.gallon input', this);

        cubic.on('input', function(){
            gallon.val(cubic.val() * CUBICMETER_GALLON_RATIO);
        });

        gallon.on('input', function(){
            cubic.val(gallon.val() / CUBICMETER_GALLON_RATIO);
        });

        let perCubic = $('.per-cubic input', this);
        let perGallon = $('.per-gallon input', this);

        perCubic.on('input', function(){
            perGallon.val(perCubic.val() / CUBICMETER_GALLON_RATIO);
        });

        perGallon.on('input', function(){
            perCubic.val(perGallon.val() * CUBICMETER_GALLON_RATIO);
        });
    });

    /**
	 * Listener to compute the total in the billing area
     */
    let totalInput = $('#input-total-billing');
    let fountainInput = $('#input-fountain-billing');
    let kioskInput = $('#input-kiosk-billing');
    let individualInput = $('#input-individual-billing');
    let computeTotal = function(){
    	let total = (parseFloat(fountainInput.val()) || 0)
						+ (parseFloat(kioskInput.val()) || 0)
						+ (parseFloat(individualInput.val()) || 0);
    	totalInput.val(total)
	};

    fountainInput.on('input', computeTotal);
    kioskInput.on('input', computeTotal);
    individualInput.on('input', computeTotal);
});