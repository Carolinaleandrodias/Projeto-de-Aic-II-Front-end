const times = [
    "07:45", "08:35", "09:45", "10:35", "11:25", "13:30", "14:20", "15:10",
    "16:20", "17:10", "18:00", "18:50", "19:40", "20:40", "21:30", "22:20"
];
let currentWeekStart = new Date();  // Start with the current date
currentWeekStart.setDate(currentWeekStart.getDate() - currentWeekStart.getDay() + 1);  // Adjust to the start of the week (Monday)

document.addEventListener('DOMContentLoaded', function() {
    updateWeekLabel();
    loadWeekBookings();

    const grid = document.getElementById('scheduleGrid');
    const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

    // Create the grid with time slots and tiles
    times.forEach(time => {
        const timeHeader = document.createElement('div');
        timeHeader.className = 'header';
        timeHeader.textContent = time;
        grid.appendChild(timeHeader);

        days.forEach(day => {
            const tile = document.createElement('div');
            tile.className = 'tile';
            tile.dataset.bookings = JSON.stringify([]);  // Initially no bookings
            tile.dataset.slot = times.indexOf(time);
            tile.dataset.day = day;
            tile.addEventListener('click', function() {
                const deleteBooking = document.getElementById('deleteBooking').checked;
                let bookings = JSON.parse(tile.dataset.bookings);
                const userBookings = bookings.filter(booking => booking.email === userEmail);

                if (deleteBooking) {
                    if (userBookings.length > 0) {
                        bookings = bookings.filter(booking => booking.email !== userEmail);
                        tile.style.backgroundColor = bookings.length ? 'orange' : '';
                        tile.innerHTML = bookings.length > 1 ? `${bookings.length} bookings` : bookings.length ? `<div>${bookings[0].email}</div><div>${bookings[0].room}</div>` : '';
                        tile.dataset.bookings = JSON.stringify(bookings);
                        // Send unbooking info to the server for each user booking
                        userBookings.forEach(booking => unbookTile(times.indexOf(time), day, booking.room));
                    }
                } else {
                    const room = document.getElementById('roomSelect').value;
                    const roomAlreadyBooked = bookings.find(booking => booking.room === room);
                    if (!roomAlreadyBooked) {
                        bookings.push({ email: userEmail, room: room });
                        tile.style.backgroundColor = 'orange';
                        tile.innerHTML = bookings.length > 1 ? `${bookings.length} bookings` : `<div>${userEmail}</div><div>${room}</div>`;
                        tile.dataset.bookings = JSON.stringify(bookings);
                        // Send booking info to the server
                        bookTile(times.indexOf(time), day, room, userEmail);
                    }
                }
            });
            grid.appendChild(tile);
        });
    });
});

function updateWeekLabel() {
    const weekLabel = document.getElementById('weekLabel');
    const endOfWeek = new Date(currentWeekStart);
    endOfWeek.setDate(endOfWeek.getDate() + 5);  // Saturday
    weekLabel.textContent = `${currentWeekStart.toLocaleDateString()} - ${endOfWeek.toLocaleDateString()}`;
}

function loadWeekBookings() {
    fetch(`/usuarios/get_bookings?start=${currentWeekStart.toISOString().split('T')[0]}`)
        .then(response => response.json())
        .then(data => {
            const grid = document.getElementById('scheduleGrid');
            grid.querySelectorAll('.tile').forEach(tile => {
                tile.style.backgroundColor = '';
                tile.innerHTML = '';
                tile.dataset.bookings = JSON.stringify([]);
            });
            data.bookings.forEach(booking => {
                const tile = grid.querySelector(`.tile[data-slot="${booking.slot}"][data-day="${booking.day}"]`);
                let bookings = JSON.parse(tile.dataset.bookings);
                bookings.push({ email: booking.email, room: booking.room });
                tile.style.backgroundColor = 'orange';
                tile.innerHTML = bookings.length > 1 ? `${bookings.length} bookings` : `<div>${booking.email}</div><div>${booking.room}</div>`;
                tile.dataset.bookings = JSON.stringify(bookings);
            });
        });
}

function bookTile(slot, day, room, email) {
    fetch('/usuarios/book_tile', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ slot, day, room, email, weekStart: currentWeekStart.toISOString().split('T')[0] })
    }).then(() => loadWeekBookings());
}

function unbookTile(slot, day, room) {
    fetch('/usuarios/unbook_tile', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ slot, day, room, weekStart: currentWeekStart.toISOString().split('T')[0] })
    }).then(() => loadWeekBookings());
}

function previousWeek() {
    currentWeekStart.setDate(currentWeekStart.getDate() - 7);
    updateWeekLabel();
    loadWeekBookings();
}

function nextWeek() {
    currentWeekStart.setDate(currentWeekStart.getDate() + 7);
    updateWeekLabel();
    loadWeekBookings();
}