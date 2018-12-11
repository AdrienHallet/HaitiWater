function drawZoneTable(){
    let baseURL = location.protocol+'//'+location.hostname+(location.port ? ':'+location.port: '');
    let dataURL = baseURL + "/api/table/?name=zones";
    console.log("Request data from: " + dataURL);
    $('#datatable-zones').DataTable(getDatatableConfiguration(dataURL));

    let table = $('#datatable-zones').DataTable();
    $('#datatable-zones tbody').on( 'click', 'tr', function () {
        if ( $(this).hasClass('selected') ) {
            $(this).removeClass('selected');
        }
        else {
            table.$('tr.selected').removeClass('selected');
            $(this).addClass('selected');
        }
    });

    $('#datatable-zones tbody').on( 'click', '.remove-row', function () {
        let data = $(this).parents('tr')[0].getElementsByTagName('td');
        if (confirm("Voulez-vous supprimer: " + data[1].innerText + ' ' + data[2].innerText + ' ?')){
            removeElement("zones", data[0].innerText);
        } else {}
    } );
    $('#datatable-zones tbody').on( 'click', '.edit-row', function () {
        let data = $(this).parents('tr')[0].getElementsByTagName('td');
        editElement(data);
    } );

    prettifyZonesHeader();
}
/**
 * Add placeholder and CSS class in the search field
 */
function prettifyZonesHeader(){
    $('#datatable-zones_filter').find('input').addClass("form-control");
    $('#datatable-zones_filter').find('input').attr("placeholder", "Recherche");
    $('#datatable-zones_filter').css("min-width", "75px");
}

function getDatatableConfiguration(dataURL){
    let config = {
        "sortable": true,
        "processing": true,
        "serverSide": true,
        "responsive": false,
        "autoWidth": false,
        scrollX:        true,
        scrollCollapse: true,
        paging:         true,
        fixedColumns:   {
            leftColumns: 1,
            rightColumns: 1
        },
        "columnDefs": [{
                "targets": -1,
                "data": null,
                "orderable": false,
                "defaultContent": getActionButtonsHTML("modalZone"),
            },
            ],
        "language": getDataTableFrenchTranslation(),
        "ajax": {
            url: dataURL
        },

        //Callbacks on fetched data
        "createdRow": function (row, data, index) {
            $('td', row).eq(5).addClass('text-center');
            $('td', row).eq(6).addClass('text-center');
        },
        "initComplete": function(settings, json){
            // Removes the last column (both header and body) if we cannot edit the table
            if(!(json.hasOwnProperty('editable') && json['editable'])){
                $('#datatable-zones').find('tr:last-child th:last-child, td:last-child').remove();
            }
        }
    };
    return config;
}
