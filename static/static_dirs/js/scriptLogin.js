document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.getElementById("login-form");
    const signupForm = document.getElementById("signup-form");

    const toggleToSignup = document.getElementById("toggle-to-signup");
    const toggleToLogin = document.getElementById("toggle-to-login");

    toggleToSignup?.addEventListener("click", function () {
        loginForm.style.display = "none";
        signupForm.style.display = "block";
    });

    toggleToLogin?.addEventListener("click", function () {
        signupForm.style.display = "none";
        loginForm.style.display = "block";
    });
});