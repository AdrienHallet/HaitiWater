document.addEventListener("DOMContentLoaded", function(event) {
    let triggerHelpAnimation = document.getElementById("trigger-help-animation");
    triggerHelpAnimation.addEventListener("mouseover", animateHelpButton, false);
    triggerHelpAnimation.addEventListener("mouseout", deanimateHelpButton, false);
    drawExampleDataTable();
    $('#content-table-help').click(function(e){
        e.stopPropagation();
    });
    $('#datatable-example-collapsible').on('click', function(){
        console.log('hello');
        setTimeout(datatableHelpTour, 1000);
    });
});

function datatableHelpTour(){
    console.log('starting tour');
    let intro = introJs();
    intro.setOptions({
        nextLabel: 'Suivant',
        prevLabel: 'Précédent',
        skipLabel: 'Passer',
        doneLabel: 'Terminer',
        steps: [
            {
                element: document.getElementsByClassName('panel-actions')[0],
                position: "left",
                intro: "Voici les boutons d'action des tables."
            },
            {
                element: document.getElementsByClassName('fa fa-plus clickable')[0],
                position: "left",
                intro: "Ce bouton ouvre un formulaire pour ajouter un élément à la table."
            },
            {
                element: document.getElementsByClassName('fa-print')[0],
                position: "left",
                intro: "Ce bouton vous permet d'imprimer les informations de la table telle qu'elle vous est présentée. Le tri, filtre et page sont conservés."
            },
            {
                element: document.getElementsByClassName('fa-cog')[0],
                position: "left",
                intro: "Ce bouton vous permet d'afficher des options avancées pour la table."
            },
            {
                element: document.getElementsByTagName('input')[0],
                position: "left",
                intro: "En écrivant dans le champ de recherche, vous filtrez la table sur toutes les colonnes."
            },
            {
                element: document.getElementsByTagName('thead')[0],
                position: "bottom",
                intro: "Les colonnes de la table peuvent être triées en cliquant dessus (ordre ascendant ou descendant)"
            },
            {
                element: document.getElementsByClassName('fa-pen')[0],
                position: "left",
                intro: "Le crayon vous permet de modifier les informations d'une entrée de la table."
            },
            {
                element: document.getElementsByClassName('fa-trash')[0],
                position: "left",
                intro: "Ce bouton vous permet de supprimer une entrée de la table."
            },
            {
                element: document.getElementsByClassName('pagination')[0],
                position: "left",
                intro: "Vous pouvez naviguer entre les pages de la table, qui par défaut n'affichent que dix entrées."
            },
        ].filter(function(obj) { return $(obj.element).length; }) // Only show step if element exists (multi-menu)
    });
    intro.start();
}

function drawExampleDataTable(){
    $('#datatable-example').DataTable({
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
        sortable: true,
        paging:         true,
        pagingType: 'full_numbers',
        "columnDefs": [{
                "targets": -1,
                "data": null,
                "orderable": false,
                "defaultContent": getActionButtonsHTML(''),
            },
            ],
        "language": getDataTableFrenchTranslation(),
    });
    prettifyHeader('example');
}

function animateHelpButton(){
    document.getElementById("quick-help").classList.add("breathing-color");
}

function deanimateHelpButton(){
    document.getElementById("quick-help").classList.remove("breathing-color");
}

