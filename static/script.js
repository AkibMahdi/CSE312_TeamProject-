document.addEventListener("DOMContentLoaded", function() {
    // Get references to the search bar and submit button
    var searchInput = document.querySelector(".search input");
    var submitButton = document.querySelector(".submit a");

    // Add click event listener to the submit button
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
    // Get references to the registration and login buttons
    var registerButton = document.getElementById("register-button");
    var loginButton = document.getElementById("login-button");

    // Add click event listeners to the buttons
    registerButton.addEventListener("click", showRegistrationForm);
    loginButton.addEventListener("click", showLoginForm);
});

function showRegistrationForm() {
    // Show the registration form and hide the login form
    document.getElementById('registration-form').style.display = 'block';
    document.getElementById('login-form').style.display = 'none';
}

function showLoginForm() {
    // Show the login form and hide the registration form
    document.getElementById('login-form').style.display = 'block';
    document.getElementById('registration-form').style.display = 'none';
}


