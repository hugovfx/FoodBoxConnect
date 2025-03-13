function toggleFields() {
    var role = document.getElementById("role").value;
    var userFields = document.getElementById("user-fields");
    var restaurantField = document.getElementById("restaurant-field");

    if (role === "restaurante") {
        userFields.style.display = "none";
        restaurantField.style.display = "block";
    } else {
        userFields.style.display = "flex";
        restaurantField.style.display = "none";
    }
}

document.addEventListener('DOMContentLoaded', function() {
    var restaurantField = document.getElementById("restaurant-field");
    restaurantField.style.display = "none";
});