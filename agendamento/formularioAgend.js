// Variáveis do modal e formulário
const agendamentoForm = document.getElementById('agendamento-form'); 
const modalOverlay = document.createElement('div');
modalOverlay.className = 'modal-overlay';
document.body.appendChild(modalOverlay);

// Função para alternar o agendamento (abrir modal)
function toggleBooking(cell) {
    const selectedDate = cell.dataset.date;
    const selectedHour = cell.dataset.hour;

    document.getElementById('data').value = selectedDate.split('T')[0];
    document.getElementById('hora').value = selectedHour.split(' - ')[0];

    showModal();
}

// Função para mostrar o modal
function showModal() {
    agendamentoForm.style.display = 'block';
    modalOverlay.style.display = 'block';
}

// Função para fechar o modal
function closeModal() {
    agendamentoForm.style.display = 'none';
    modalOverlay.style.display = 'none';
}

// Evento de clique para fechar o modal ao clicar fora dele
modalOverlay.addEventListener('click', closeModal);

// Carregar as opções das salas de aulas a partir de JSON
document.addEventListener('DOMContentLoaded', () => {
    fetch('/dados/salas.json')
        .then(response => response.json())
        .then(salas => {
            const salaSelect = document.getElementById('sala');
            salas.forEach(sala => {
                const option = document.createElement('option');
                option.value = sala.id;
                option.textContent = sala.nome;
                salaSelect.appendChild(option);
            });
        })
        .catch(error => console.error('Erro ao carregar as salas:', error));
});

// Array para armazenar agendamentos
const agendamentos = [];

// Função para armazenar os dados de agendamento
function storeBookingData(event) {
    event.preventDefault();

    const nome = document.getElementById('nome').value;
    const data = document.getElementById('data').value;
    const hora = document.getElementById('hora').value;
    const sala = document.getElementById('sala').value;

    const agendamento = { nome, data, hora, sala };

    agendamentos.push(agendamento);
    console.log('Agendamento realizado:', agendamento);

    closeModal();
    document.getElementById('agendamentoForm').reset();
}
