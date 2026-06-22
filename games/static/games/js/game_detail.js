// Pega os dois elementos pelos ids que colocamos no HTML
const descricao = document.getElementById('game-description');
const botao = document.getElementById('read-more-btn');


// Quando clicar no botão...
botao.addEventListener("click", () => {
    // liga/desliga a classe "expanded" na descrição
    descricao.classList.toggle("expanded");

    // troca o texto do botão conforme o estado atual
    if (descricao.classList.contains("expanded")) {
        botao.textContent = "Ver menos ▴";
    } else {
        botao.textContent = "Ver mais ▾";
    }
});