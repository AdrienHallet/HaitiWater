/**
 * Created by celine on 27/11/18.
 */

/**
 * Validate (check if valid) the form.
 * If not valid, display messages
 */
function validateForm() {
    let form = document.forms["form-connect-user"];

    let username = form["username"].value;
    let password = form["pwd"].value;

    let missing = false;
    /*if (type === "none") {
        document.getElementById("select-type-error").className = "error";
        missing = true;
    }
    if (username.trim() === "") {
        document.getElementById("input-localization-error").className = "error";
        missing = true;
    }
    if (state === "none") {
        document.getElementById("select-state-error").className = "error";
        missing = true;
    }*/

    if(missing){
        return false
    } else {
        return buildRequest(username, password);
    }

}

/**
 * Build the request
 */
function buildRequest(username, password){
    let request = "table=user_connect";
    request += "&username=" + username;
    request += "&password=" + password;

    return request;
}

function authUser(){
    console.log("Poke ?")
    let request = validateForm();
    if(!request){
        // Form is not valid (missing/wrong fields)
        return false;
    }
    let baseURL = location.protocol+'//'+location.hostname+(location.port ? ':'+location.port: '');
    let postURL = baseURL + "/user/connect/";
    let xhttp = new XMLHttpRequest();
    xhttp.open("POST", postURL, true);
    xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    xhttp.onreadystatechange = function() {
        if(xhttp.readyState !== 4 || xhttp.status !== 200) {
            if(xhttp.responseText) {
                new PNotify({
                title: 'Échec!',
                text: 'La connexion a échoué',
                type: 'failure'
                });
                console.log("POST error on connection");
            }
        } else {
            window.localStorage.setItem("token", JSON.parse(xhttp.response).token);
            window.localStorage.setItem("group", JSON.parse(xhttp.response).group);
            window.localStorage.setItem("zone", JSON.parse(xhttp.response).zone_name);
            window.localStorage.setItem("zoneId", JSON.parse(xhttp.response).zone_id);
            window.localStorage.setItem("userName", JSON.parse(xhttp.response).user_name);
            window.location.replace(baseURL+"/accueil/")
        }
    };
    xhttp.send(request)
}