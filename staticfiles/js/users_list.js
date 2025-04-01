document.addEventListener("DOMContentLoaded", function () {
    const rowsPerPage = 5;
    let currentPage = 1;
    const tableBody = document.getElementById("usuarios-body");
    const rows = Array.from(tableBody.getElementsByTagName("tr"));
    const totalPages = Math.ceil(rows.length / rowsPerPage);
    const pageInfo = document.getElementById("page-info");

    function showPage(page) {
        const start = (page - 1) * rowsPerPage;
        const end = start + rowsPerPage;
        rows.forEach((row, index) => {
            row.style.display = index >= start && index < end ? "table-row" : "none";
        });
        pageInfo.textContent = `Página ${page} de ${totalPages}`;
        document.getElementById("prev-page").disabled = page === 1;
        document.getElementById("next-page").disabled = page === totalPages;
    }

    window.changePage = function (step) {
        if ((step === -1 && currentPage > 1) || (step === 1 && currentPage < totalPages)) {
            currentPage += step;
            showPage(currentPage);
        }
    };

    showPage(currentPage);
});

function confirmarGuardado() {
    return confirm("¿Estás seguro de que quieres guardar los cambios?");
}