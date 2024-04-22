document.addEventListener("DOMContentLoaded", function() {
    
    var searchInput = document.querySelector(".search input");
    var submitButton = document.querySelector(".submit a");

    
    submitButton.addEventListener("click", function(event) {
        event.preventDefault(); 
        toggleSearch(); 
    });


    function toggleSearch() {
        if (searchInput.style.display === "none" || searchInput.style.display === "") {
            searchInput.style.display = "block"; 
        } else {
            searchInput.style.display = "none"; 
        }
    }
});

document.addEventListener("DOMContentLoaded", function() {

    var registerButton = document.getElementById("register-button");
    var loginButton = document.getElementById("login-button");

    registerButton.addEventListener("click", showRegistrationForm);
    loginButton.addEventListener("click", showLoginForm);
});

function showRegistrationForm() {
    
    document.getElementById('registration-form').style.display = 'block';
    document.getElementById('login-form').style.display = 'none';
}

function showLoginForm() {
    
    document.getElementById('login-form').style.display = 'block';
    document.getElementById('registration-form').style.display = 'none';
}

