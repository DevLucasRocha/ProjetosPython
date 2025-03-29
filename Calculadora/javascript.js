// Constante com a URL base da API
const API_BASE_URL = 'http://localhost:5000';

async function calculate() {
    // ... (código anterior) ...
    
    // Modifique a chamada fetch para:
    const response = await fetch(`${API_BASE_URL}/api/calcular`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
        mode: 'cors'  // Adicione esta linha
    });
    
    // ... (restante do código) ...
}

async function loadHistory() {
    try {
        // Modifique esta chamada:
        const response = await fetch(`${API_BASE_URL}/api/historico`, {
            mode: 'cors'  // Adicione esta linha
        });
        // ... (restante do código) ...
    } catch (error) {
        console.error('Erro ao carregar histórico:', error);
        historyList.innerHTML = '<div class="history-item">Erro ao carregar histórico. Verifique se o back-end está rodando.</div>';
    }
}

async function clearHistory() {
    try {
        // Modifique esta chamada:
        await fetch(`${API_BASE_URL}/api/limpar_historico`, {
            method: 'POST',
            mode: 'cors'  // Adicione esta linha
        });
        loadHistory();
    } catch (error) {
        console.error('Erro ao limpar histórico:', error);
        alert('Erro ao limpar histórico');
    }
}