'use strict';
let monthlyReportNotification = '' +
    '<a href="../rapport" class="clearfix">' +
        '<div class="image">' +
        '</div>' +
        '<span class="title">Rapport en attente</span>' +
        '<span class="message">Un rapport est en attente,' +
            'visitez la page des rapports pour l\'envoyer.</span>' +
    '</a>';

$( document ).ready(function() {

    //Get local storage value or true (as it is default to be open)
    let isMenuOpen = (localStorage.getItem('isMenuOpen') === 'true');
    if(!isMenuOpen){
        $('html').addClass('sidebar-left-collapsed')
    }

    //Toggle menu position on localstorage to save collapsed state
    $('.sidebar-toggle').on('click', function (){
        isMenuOpen = !isMenuOpen;
        localStorage.setItem('isMenuOpen', isMenuOpen.toString());
    })

    setupNotifications();
});

function setupNotifications(){
    let notificationParent = $('#notification-parent');
    let notificationList = $('#notification-content');
    let alertBadge = $('#alert-badge');
    let classicBadge = $('#classic-badge')

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
        appendNotification(notificationList, monthlyReportNotification);
        return true;
    }
    return false;
}

function appendNotification(notificationList, notification){
    let wrappedNotification = '<li>' + notification + '</li>';
    notificationList.append(wrappedNotification);
}
