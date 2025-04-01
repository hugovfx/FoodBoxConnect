function togglePassword() {
    const passwordInput = document.getElementById("password");
    const eyeIcon = document.getElementById("eyeIcon");

    if (passwordInput.type === "password") {
        passwordInput.type = "text";
        passwordInput.placeholder = "password"
        eyeIcon.classList.remove("fa-eye-slash"); 
        eyeIcon.classList.add("fa-eye");
    } else {
        passwordInput.type = "password";
        passwordInput.placeholder = "********"
        eyeIcon.classList.remove("fa-eye");
        eyeIcon.classList.add("fa-eye-slash");
    }
}