// Função para aceitar pedido
function aceitarPedido(id) {
    console.log(`Pedido ${id} aceito.`);
    // Integração com backend aqui
}

// Função para rejeitar pedido
function rejeitarPedido(id) {
    console.log(`Pedido ${id} rejeitado.`);
    // Integração com backend aqui
}

// Função para abrir armário
function abrirArmario(id) {
    console.log(`Armário ${id} aberto.`);
    // Integração com backend aqui
}

// Função para remover armário
function removerArmario(id) {
    console.log(`Armário ${id} removido.`);
    // Integração com backend aqui
}

// Logout
document.getElementById('logout').addEventListener('click', () => {
    console.log('Usuário deslogado.');
    window.location.href = 'index.html';
});