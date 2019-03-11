document.addEventListener("DOMContentLoaded", function(event) {
    let triggerHelpAnimation = document.getElementById("trigger-help-animation");
    triggerHelpAnimation.addEventListener("mouseover", animateHelpButton, false);
    triggerHelpAnimation.addEventListener("mouseout", deanimateHelpButton, false);

});

function animateHelpButton(){
    document.getElementById("quick-help").classList.add("breathing-color");
}

function deanimateHelpButton(){
    document.getElementById("quick-help").classList.remove("breathing-color");
}

