/**
 * Handles the forms of the profile modification
 */
$(document).ready(function() {
    let password = document.getElementById("input-new-password")
        , confirm_password = document.getElementById("input-new-password-confirm");

    function validatePassword() {
        if (password.value !== confirm_password.value) {
            confirm_password.setCustomValidity("Les mots de passe ne sont pas identiques !");
        } else {
            confirm_password.setCustomValidity('');
        }
    }

    password.onchange = validatePassword;
    confirm_password.onkeyup = validatePassword;
});