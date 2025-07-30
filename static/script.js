async function fetchStatus() {
    const res = await fetch('/status');
    const data = await res.json();
    renderHotel(data);
}

function renderHotel(data) {
    const container = document.getElementById('hotel');
    container.innerHTML = '';

    Object.keys(data).sort((a, b) => b - a).forEach(floor => {
        const floorDiv = document.createElement('div');
        floorDiv.className = 'floor';

        data[floor].forEach(room => {
            const roomDiv = document.createElement('div');
            roomDiv.className = 'room';
            if (room.booked) roomDiv.classList.add('booked');
            roomDiv.textContent = room.room;
            floorDiv.appendChild(roomDiv);
        });

        container.appendChild(floorDiv);
    });
}

async function bookRooms() {
    const count = document.getElementById('roomCount').value;
    const res = await fetch('/book', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ count })
    });
    const data = await res.json();
    alert(data.message || `Booked: ${data.booked_rooms.join(', ')}`);
    fetchStatus();
}

async function randomize() {
    await fetch('/randomize', { method: 'POST' });
    fetchStatus();
}

async function reset() {
    await fetch('/reset', { method: 'POST' });
    fetchStatus();
}

fetchStatus();
