document.addEventListener("DOMContentLoaded", function () {
    const formTitle = document.getElementById("form-title-no-bootstrap");
    const nameInput = document.getElementById("name");
    const nameInputGroup = nameInput.parentElement; // Get the wrapper div (icon + input)
    const submitBtn = document.getElementById("submit-btn");
    const toggleBtn = document.getElementById("toggle-btn");
    const toggleText = toggleBtn.parentElement;
    let isRegister = false;

    function toggleForm() {
        isRegister = !isRegister;

        if (isRegister) {
            formTitle.textContent = "Create an Account";
            nameInputGroup.style.display = "block"; // Show name input and icon
            submitBtn.textContent = "Sign Up";
            toggleText.innerHTML = `Already have an account? <span id="toggle-btn">Login</span>`;
        } else {
            formTitle.textContent = "Welcome Back";
            nameInputGroup.style.display = "none"; // Hide name input and icon
            submitBtn.textContent = "Login";
            toggleText.innerHTML = `Don't have an account? <span id="toggle-btn">Sign Up</span>`;
        }

        // Reattach event listener after replacing HTML content
        document.getElementById("toggle-btn").addEventListener("click", toggleForm);
    }

    // Attach the event listener
    toggleBtn.addEventListener("click", toggleForm);

    // Ensure the name input is hidden on page load (default to login)
    nameInputGroup.style.display = "none";
});
