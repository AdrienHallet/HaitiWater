/**
 * Full page tour for dashboard.
 * Is a standalone, to not trigger on each page using the layout
 */
function startPageTour() {
    let intro = introJs();
    intro.setOptions({
        nextLabel: 'Suivant',
        prevLabel: 'Précédent',
        skipLabel: 'Passer',
        doneLabel: 'Terminer',
        showStepNumbers: false,
        steps: [
            {
                intro: "Bienvenue sur HaïtiWater !<br>" +
                    "Cette introduction va vous présenter rapidement l'interface de l'application."
            },
            {
                element: document.getElementById('menu-dashboard'),
                position: "right",
                intro: "Vous êtes ici."
            },
            {
                element: document.getElementById('menu-water-network'),
                position: "right",
                intro: "Consultez et modifiez les éléments du réseau de distribution."
            },
            {
                element: document.getElementById('menu-map'),
                position: "right",
                intro: "Consultez et modifiez les éléments du réseau sous forme de carte !"
            },
            {
                element: document.getElementById('menu-zone-management'),
                position: "right",
                intro: "Gérez les zones et gestionnaires de l'application."
            },
            {
                element: document.getElementById('menu-logs'),
                position: "right",
                intro: "Acceptez ou refusez les changements de vos subordonnés."
            },
            {
                element: document.getElementById('menu-report'),
                position: "right",
                intro: "Envoyez les données mensuelles de volume et rapportez les problèmes liés au réseau de distribution."
            },
            {
                element: document.getElementById('menu-consumers'),
                position: "right",
                intro: "Consultez et modifiez vos consommateurs."
            },
            {
                element: document.getElementById('menu-financial'),
                position: "right",
                intro: "Gérez les paiements de vos consommateurs."
            },
            {
                element: document.getElementById('menu-help'),
                position: "right",
                intro: "La documentation complète vous attend si nécessaire."
            },
            {
                element: document.getElementById('notification-parent'),
                position: "bottom",
                intro: "Les notifications s'afficheront ici."
            },
            {
                element: document.getElementById('userbox'),
                position: "bottom",
                intro: "Vous pouvez modifiez votre profil, mot de passe, et vous déconnecter avec ce menu."
            },
        ].filter(function(obj) { return $(obj.element).length; }) // Only show step if element exists (multi-menu)
    });
    intro.start();
}