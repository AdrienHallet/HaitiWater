function setWaterDataTableURL(month){
    let baseURL = location.protocol+'//'+location.hostname+(location.port ? ':'+location.port: '');
    let dataURL = baseURL + "/api/table/?name=water_element&month=" + month;
    $('#datatable-water_element').DataTable().ajax.url(dataURL).load();
}

function drawWaterElementTable(withManagers, withActions, gis){
    let baseURL = location.protocol+'//'+location.hostname+(location.port ? ':'+location.port: '');
    let dataURL = baseURL + "/api/table/?name=water_element&month=none";
    console.log("Request data from: " + dataURL);
    let configuration;
    if(gis){
        configuration = getWaterDatatableGISConfiguration(dataURL, withManagers, withActions);
    }
    else {
        configuration = getWaterDatatableConfiguration(dataURL, withManagers, withActions);
    }
    $('#datatable-water_element').DataTable(configuration);

    let table = $('#datatable-water_element').DataTable();
    $('#datatable-water_element tbody').on( 'click', 'tr', function () {
        if ( $(this).hasClass('selected') ) {
            $(this).removeClass('selected');
        }
        else {
            table.$('tr.selected').removeClass('selected');
            $(this).addClass('selected');
        }
    });

    $('#datatable-water_element tbody').on( 'click', '.remove-row', function () {
        let data = $(this).parents('tr')[0].getElementsByTagName('td');
        if (confirm("Voulez-vous supprimer: " + data[1].innerText + ' ' + data[2].innerText + ' ?')){
            removeElement("water_element", data[0].innerText);
        } else {}
    } );
    $('#datatable-water_element tbody').on( 'click', '.edit-row', function () {
        let data = $(this).parents('tr')[0].getElementsByTagName('td');
        editElement(data);
    } );
    prettifyHeader('water_element');
}

function getWaterDatatableConfiguration(dataURL, withManagers, withActions){
    let config = {
        lengthMenu: [
            [ 10, 25, 50, -1 ],
            [ '10', '25', '50', 'Tout afficher' ]
        ],
        dom: 'Bfrtip',
        buttons: [
            {
                extend: 'print',
                exportOptions: {
                    columns: [0,1,2,3,4,5,6,7],
                },
            },
            {
                text: 'Volume total',
                attr:{
                    id: 'water-element-month-selector',
                }
            },
            'pageLength',

        ],
        sortable: true,
        processing: true,
        serverSide: true,
        responsive: true,
        autoWidth: true,
        scrollX:        true,
        scrollCollapse: true,
        paging:         true,
        pagingType: 'full_numbers',
        fixedColumns:   {
            leftColumns: 1,
            rightColumns: 1
        },
        columnDefs: [
            {
                targets: -1, // Actions column
                data: null,
                sortable: false,
                defaultContent: getActionButtonsHTML('modalWaterElement'),
            },
            {
                targets: -2, // Zone column
                visible: true,
                defaultContent: 'Pas de zone',

            },
            {
                targets: -3, // Manager column
                defaultContent: 'Pas de gestionnaire',
                visible: withManagers,
            }
            ],
        language: getDataTableFrenchTranslation(),
        ajax: {
            url: dataURL
        },

        //Callbacks on fetched data
        "createdRow": function (row, data, index) {
            $('td', row).eq(5).addClass('text-center');
            $('td', row).eq(6).addClass('text-center');
            //Hide actions if column hidden
            if ($("#datatable-water_element th:last-child, #datatable-ajax td:last-child").hasClass("hidden")){
                $('td', row).eq(8).addClass('hidden');
            }
            if (withManagers) {
                $('td', row).eq(7).addClass('text-center');
            }
        },
        "initComplete": function(settings, json){
            // Removes the last column (both header and body) if we cannot edit or if required by withAction argument
            console.log(json['editable']);
            if(!withActions || !(json.hasOwnProperty('editable') && json['editable'])){
                $('#datatable-water_element').DataTable().column(-1).visible(false);

            }
        }
    };
    return config;
}

function getWaterDatatableGISConfiguration(dataURL, withManagers, withActions){
    let config = {
        lengthMenu: [
            [ 10, 25, 50, -1 ],
            [ '10', '25', '50', 'Tout afficher' ]
        ],
        dom: 'Bfrtip',
        buttons: [
            {
                extend: 'print',
                exportOptions: {
                    columns: [0,1,2,3,4,5,6,7],
                },
            },
            {
                text: 'Volume total',
                attr:{
                    id: 'water-element-month-selector',
                }
            },
            'pageLength',

        ],
        sortable: true,
        processing: true,
        serverSide: true,
        responsive: true,
        autoWidth: true,
        scrollX:        true,
        scrollCollapse: true,
        paging:         true,
        pagingType: 'full_numbers',
        fixedColumns:   {
            leftColumns: 1,
            rightColumns: 1
        },
        columnDefs: [
            {
                targets: -1, // Actions column
                data: null,
                sortable: false,
                defaultContent: getActionButtonsHTML('modalWaterElement'),
            },
            {
                targets: -2, // Zone column
                visible: true,
                defaultContent: 'Pas de zone',

            },
            {
                targets: -3, // Manager column
                defaultContent: 'Pas de gestionnaire',
                visible: false,
            },
            {
                targets: [3,4,5,6,7], // User count
                visible: false,
            }
            ],
        language: getDataTableFrenchTranslation(),
        ajax: {
            url: dataURL
        },

        //Callbacks on fetched data
        "createdRow": function (row, data, index) {
            $('td', row).eq(5).addClass('text-center');
            $('td', row).eq(6).addClass('text-center');
            //Hide actions if column hidden
            if ($("#datatable-water_element th:last-child, #datatable-ajax td:last-child").hasClass("hidden")){
                $('td', row).eq(8).addClass('hidden');
            }
            if (withManagers) {
                $('td', row).eq(7).addClass('text-center');
            }
        },
        "initComplete": function(settings, json){
            // Removes the last column (both header and body) if we cannot edit or if required by withAction argument
            console.log(json['editable']);
            if(!withActions || !(json.hasOwnProperty('editable') && json['editable'])){
                $('#datatable-water_element').DataTable().column(-1).visible(false);

            }
        }
    };
    return config;
}

$(document).ready(function() {
    attachMonthSelectorHandler();
});

function attachMonthSelectorHandler(){
    let button = $('#water-element-month-selector');
    button.datepicker({
        format: "mm-yyyy",
        startView: "months",
        minViewMode: "months",
    });
    button.on('changeDate', function (e) {
        console.log("click");
        let month = e.format();
        if (month.length < 1) {
            // Month de-selected
            month = 'none';
            console.log(button);
            button[0].innerText = 'Volume total';
        }
        else {
            button[0].innerText = formatButton(month);
        }
        setWaterDataTableURL(month);
    });
}

function formatButton(monthYear){
    const monthNames = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
      "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"
    ];
    let params = monthYear.split("-");
    let yearInt = params[1];
    let monthInt = parseInt(params[0]) - 1;
    return monthNames[monthInt]+ " " + yearInt;
}
