document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    const submitButton = form.querySelector("button[type='submit']");

    form.addEventListener("submit", function () {
        submitButton.disabled = true;
        submitButton.textContent = "Registrando..."; // Mensaje opcional
    });
});
