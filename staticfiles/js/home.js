let timeout;

    document.getElementById("button-toggle").addEventListener("click", function(event) {
        event.preventDefault();
        let buttonToggle = document.getElementById('button-toggle');
        let buttonSearch = document.getElementById('button-search');
        let input = document.getElementById("input-search");

        buttonToggle.style.display = "none";
        buttonSearch.style.display = "block";
        input.style.display = "inline-block";
        setTimeout(() => input.classList.add("visible"), 10);

        input.focus();
        iniciarTemporizador();
    });

    document.getElementById("input-search").addEventListener("input", function() {
        clearTimeout(timeout);
        if (this.value.trim() === "") {
            iniciarTemporizador();
        }
    });

    function iniciarTemporizador() {
        timeout = setTimeout(() => {
            let buttonToggle = document.getElementById('button-toggle');
            let buttonSearch = document.getElementById('button-search');
            let input = document.getElementById("input-search");

            if (input.value.trim() === "") {
                input.classList.add("hidden"); // Primero reduce su tamaño
                
                setTimeout(() => {
                    input.style.display = "none"; // Luego lo oculta por completo
                    input.classList.remove("visible", "hidden"); // Limpia las clases
                    buttonToggle.style.display = "block"; // Restaura el botón original
                    buttonSearch.style.display = "none"; // Oculta el botón de búsqueda
                    input.value = ""; // Asegura que el input esté limpio
                }, 500); // Espera 0.5s para coincidir con la transición
            }
        }, 5000); // Espera 5 segundos antes de ocultar
    }