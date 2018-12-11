function drawManagersTable(){
    let baseURL = location.protocol+'//'+location.hostname+(location.port ? ':'+location.port: '');
    let dataURL = baseURL + "/api/table/?name=managers";
    console.log("Request data from: " + dataURL);
    $('#datatable-managers').DataTable(getManagersDatatableConfiguration(dataURL));

    let table = $('#datatable-managers').DataTable();
    $('#datatable-managers tbody').on( 'click', 'tr', function () {
        if ( $(this).hasClass('selected') ) {
            $(this).removeClass('selected');
        }
        else {
            table.$('tr.selected').removeClass('selected');
            $(this).addClass('selected');
        }
    });

    $('#datatable-managers tbody').on( 'click', '.remove-row', function () {
        let data = $(this).parents('tr')[0].getElementsByTagName('td');
        if (confirm("Voulez-vous supprimer: " + data[1].innerText + ' ' + data[2].innerText + ' ?')){
            removeElement("managers", data[0].innerText);
        } else {}
    } );
    $('#datatable-managers tbody').on( 'click', '.edit-row', function () {
        let data = $(this).parents('tr')[0].getElementsByTagName('td');
        editElement(data);
    } );

    prettifyManagersHeader();
}
/**
 * Add placeholder and CSS class in the search field
 */
function prettifyManagersHeader(){
    $('#datatable-managers_filter').find('input').addClass("form-control");
    $('#datatable-managers_filter').find('input').attr("placeholder", "Recherche");
    $('#datatable-managers_filter').css("min-width", "300px");
}

function getManagersDatatableConfiguration(dataURL){
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
                "defaultContent": getActionButtonsHTML("modalManager"),
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
                $('#datatable-managers').find('tr:last-child th:last-child, td:last-child').remove();
            }
        }
    };
    return config;
}
