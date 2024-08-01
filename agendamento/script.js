
const scheduleGrid = document.getElementById('scheduleGrid');
const weekLabel = document.getElementById('weekLabel');

let currentDate = new Date();
const weekDays = ['Domingo','Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira','Sabado'];
//const rooms = ['Sala 1', 'Sala 2', 'Sala 3', 'Sala 4', 'Sala 5'];
const hours = Array.from({ length: 12 }, (_, i) => `${String(i + 8).padStart(2, '0')}:00 - ${String(i + 9).padStart(2, '0')}:00`);

function generateWeekDates(date) {
    // Cria uma nova data baseada na data fornecida
    const startOfWeek = new Date(date);
    
    // Semana começa no domingo
    startOfWeek.setDate(startOfWeek.getDate() - startOfWeek.getDay());
    
    // Cria um array de 7 elementos para os dias úteis (segunda a domingo)
    return Array.from({ length: 7 }, (_, i) => {
        if (i !== 0) {
            startOfWeek.setDate(startOfWeek.getDate() +1);
        }
        return new Date(startOfWeek);
    });
}
// function generateWeekDates(date) {
//     const startOfWeek = new Date(date);
//     startOfWeek.setDate(startOfWeek.getDate() - startOfWeek.getDay());
//     return Array.from({ length: 7 }, (_, i) => new Date(startOfWeek.setDate(startOfWeek.getDate() + (i === 0 ? 0 : 1))));
// }

function renderSchedule() {
    scheduleGrid.innerHTML = '';
    const weekDates = generateWeekDates(currentDate);

    // Cabeçalho - header
    scheduleGrid.appendChild(createElement('div', 'header', 'Horários'));
    weekDates.forEach(date => {
        scheduleGrid.appendChild(createElement('div', 'header', `${weekDays[date.getDay()]} \n ${date.getUTCDate()}`));
    });

    // Marcação das cells
    hours.forEach(hour => {
        scheduleGrid.appendChild(createElement('div', 'time', hour));
        weekDates.forEach(date => {
                const cell = createElement('div', 'cell available', '');
                cell.dataset.date = date.toISOString();
                cell.dataset.hour = hour;
                cell.onclick = () => toggleBooking(cell);
                scheduleGrid.appendChild(cell);
            
        });
    });

    updateWeekLabel(); 
}

function createElement(tag, className, text) {
    const element = document.createElement(tag);
    element.className = className;
    element.innerText = text;
    return element;
}

function toggleBooking(cell) {
    if (cell.classList.contains('available')) {
        cell.classList.remove('available');
        cell.classList.add('booked');
    } else {
        cell.classList.remove('booked');
        cell.classList.add('available');
    }
}

function previousWeek() {
    currentDate.setDate(currentDate.getDate() - 7);
    renderSchedule();
}

function nextWeek() {
    currentDate.setDate(currentDate.getDate() + 7);
    renderSchedule();
}

function updateWeekLabel() {
    const weekDates = generateWeekDates(currentDate);
    weekLabel.innerText = `Semana de ${weekDates[0].toLocaleDateString()} a ${weekDates[6].toLocaleDateString()}`;
}

document.addEventListener('DOMContentLoaded', () => {
    renderSchedule();
});

