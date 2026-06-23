document.querySelectorAll('.progress-fill').forEach(function (barra) {
    barra.style.width = barra.dataset.progress + '%';
});