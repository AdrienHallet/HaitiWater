function drawManagerTable(){
    let baseURL = location.protocol+'//'+location.hostname+(location.port ? ':'+location.port: '');
    let dataURL = baseURL + "/api/table/?name=manager";
    console.log("Request data from: " + dataURL);
    $('#datatable-manager').DataTable(getManagerDatatableConfiguration(dataURL));

    let table = $('#datatable-manager').DataTable();
    $('#datatable-manager tbody').on( 'click', 'tr td:not(:last-child)', function () {
        let row = $(this).closest('tr');
        if ( row.hasClass('selected') ) {
            row.removeClass('selected');
            filterWaterElementFromManager(table);
        }
        else {
            table.$('tr.selected').removeClass('selected');
            row.addClass('selected');
            filterWaterElementFromManager(table);
        }
    });

    $('#datatable-manager tbody').on( 'click', '.remove-row', function () {
        let data = $(this).parents('tr')[0].getElementsByTagName('td');
        if (confirm("Voulez-vous supprimer: " + data[1].innerText + ' ' + data[2].innerText + ' ?')){
            removeElement("manager", data[0].innerText);
        } else {}
    } );
    $('#datatable-manager tbody').on( 'click', '.edit-row', function () {
        let data = table.row($(this).closest('tr')).data();
        setupModalManagerEdit(data);
    } );

    prettifyHeader('manager');
}

function filterWaterElementFromManager(managerTable){
    let data = managerTable.row('tr.selected').data();

    if  (data == null){ // If nothing selected
        $('#datatable-water_element').DataTable().search("").draw();
        return;
    }
    let managerType = data[4];
    let managerZone = data[5];
    let managerId = data[0];
    if (managerType.includes('fontaine')){
        // Filter on the manager if he's a fountain manager
        $('#datatable-water_element').DataTable().search(managerId).draw();
    } else {
        // Filter on the zone if he's a zone manager
        $('#datatable-water_element').DataTable().search(managerZone).draw();
    }

}

function getManagerDatatableConfiguration(dataURL){
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
                    columns: [0,1,2,3,4,5,6],
                },
            },
            'pageLength'
        ],
        "sortable": true,
        "processing": true,
        "serverSide": true,
        "responsive": false,
        "autoWidth": true,
        scrollX:        true,
        scrollCollapse: true,
        paging:         true,
        pagingType: 'full_numbers',
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
        "ajax": getAjaxController(dataURL),

        //Callbacks on fetched data
        "createdRow": function (row, data, index) {
            $('td', row).eq(5).addClass('text-center');
            $('td', row).eq(6).addClass('text-center');
        },
        "initComplete": function(settings, json){
            // Removes the last column (both header and body) if we cannot edit the table
            if(!(json.hasOwnProperty('editable') && json['editable'])){
                $('#datatable-manager').find('tr:last-child th:last-child, td:last-child').remove();
            }
        }
    };
    return config;
}
