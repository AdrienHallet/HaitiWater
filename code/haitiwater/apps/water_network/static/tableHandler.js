/**
 * Custom Table Handler
 * Used to prettify the table and make it respond to custom input and commands
 *
 */

// (function( $ ) {
//
// 	'use strict';
//
// 	let baseURL = location.protocol+'//'+location.hostname+(location.port ? ':'+location.port: '');
//     let dataURL = baseURL + "/api/table/?name=water_element";
//     console.log(dataURL);
// 	var datatableInit = function() {
//
// 		var $table = $('#datatable-ajax');
// 		$table.dataTable({
// 			bProcessing: true,
// 			sAjaxSource: $table.data(dataURL)
// 		});
//
// 	};
//
// 	$(function() {
// 		datatableInit();
// 	});
//
// }).apply( this, [ jQuery ]);

$(document).ready(function() {
    let baseURL = location.protocol+'//'+location.hostname+(location.port ? ':'+location.port: '');
    let dataURL = baseURL + "/api/table/?name=water_element";
    console.log(dataURL);
    $('#datatable-ajax').DataTable( {
        "processing": true,
        "serverSide": true,
        "ajax": dataURL
    } );
} );