function togglePasswordVisibility(){
    let passwordField = document.getElementById('id_password');
    let toggleIcon = document.getElementById('password-visibility-toggle');
    if (passwordField.type === "password"){
        passwordField.type = "text";
        console.log(toggleIcon);
        toggleIcon.classList.replace('fa-eye', 'fa-eye-slash');
    } else {
        passwordField.type = "password";
        toggleIcon.classList.replace('fa-eye-slash', 'fa-eye');
    }
}