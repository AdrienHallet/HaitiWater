'use strict';
$( document ).ready(function() {

    //Get local storage value or true (as it is default to be open)
    let localMenu = localStorage.getItem('isMenuOpen');
    let isMenuOpen = (localMenu === 'true' || localMenu === null);
    if(!isMenuOpen){
        $('html').addClass('sidebar-left-collapsed')
    }

    //Toggle menu position on localstorage to save collapsed state
    $('.sidebar-toggle').on('click', function (){
        isMenuOpen = !isMenuOpen;
        localStorage.setItem('isMenuOpen', isMenuOpen.toString());
    });

    $('[data-toggle="tooltip"]').tooltip();

    setupNotifications();
});

/**
 * Requests notification computings and modifies the counters to alert the user
 */
function setupNotifications(){
    let notificationParent = $('#notification-parent');
    let notificationList = $('#notification-content');
    let alertBadge = $('#alert-badge');
    let classicBadge = $('#classic-badge');

    let notificationCounter = 0;
    if (notificationMonthlyReport(notificationList)) notificationCounter += 1;

    classicBadge.html(notificationCounter);
    alertBadge.html(notificationCounter);

    if (notificationCounter > 0){
        notificationParent.find('.badge').removeClass('hidden');
    }
    else {
        notificationParent.find('.badge').addClass('hidden');
    }

}

/**
 * Adds a monthly report notification if one is waiting
 * @return {boolean} true if a notification has been set, false otherwise
 */
function notificationMonthlyReport(notificationList){
    console.log(localStorage.getItem('monthlyReport'));
    let hasMonthlyReport = (localStorage.getItem('monthlyReport') !== null);
    if (hasMonthlyReport){
        let title = 'Rapport en attente';
        let msg = 'Un rapport est en attente, visitez la page des rapports pour l\'envoyer.'
        monthlyReportNotification = formatNotification(title, msg)
        appendNotification(notificationList, monthlyReportNotification);
        return true;
    }
    return false;
}

/**
 * Appends the notification to the list
 * @param  {[type]} notificationList the list to which append the notification
 * @param  {[type]} notification     a notification (use the format for better visuals)
 */
function appendNotification(notificationList, notification){
    let wrappedNotification = '<li>' + notification + '</li>';
    notificationList.append(wrappedNotification);
}

/**
 * Format a notification to keep same visuals
 * @param  {String} title The title (most visible) information
 * @param  {String} msg   Message content
 * @return {String}       The notification with its theme format
 */
function formatNotification(title, msg){
    return '<a href="../rapport" class="clearfix">' +
        '<div class="image">' + // available for a small picture or icon
        '</div>' +
        '<span class="title">'+ title +'</span>' +
        '<span class="message">' + msg + '</span>' +
    '</a>';
}

/**
 * Intro.JS page tour start
 */
function startPageTour(){
    introJs().setOptions({
        nextLabel: 'Suivant',
        prevLabel: 'Précédent',
        skipLabel: 'Passer',
        doneLabel: 'Terminer',
    }).start();
}
