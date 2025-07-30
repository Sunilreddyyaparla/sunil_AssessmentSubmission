from flask import Flask, request, jsonify, render_template
import random

app = Flask(__name__)

# Global room structure: {floor: [room numbers and status]}
hotel_rooms = {}

# Initialize rooms: Floors 1-9 have 10 rooms, Floor 10 has 7 rooms
def initialize_rooms():
    global hotel_rooms
    hotel_rooms = {}
    for floor in range(1, 10):
        hotel_rooms[floor] = [{'room': floor * 100 + i, 'booked': False} for i in range(1, 11)]
    hotel_rooms[10] = [{'room': 1000 + i, 'booked': False} for i in range(1, 8)]

initialize_rooms()

# Calculate travel time between rooms
def calculate_travel_time(rooms):
    if not rooms:
        return float('inf')
    rooms = sorted(rooms)
    vertical_floors = abs(rooms[-1] // 100 - rooms[0] // 100)
    horizontal_rooms = abs((rooms[-1] % 100) - (rooms[0] % 100))
    return vertical_floors * 2 + horizontal_rooms * 1

# Booking logic
def find_best_rooms(requested):
    best_choice = None
    best_time = float('inf')

    # Check same-floor options first
    for floor, rooms in hotel_rooms.items():
        available = [r['room'] for r in rooms if not r['booked']]
        for i in range(len(available) - requested + 1):
            selection = available[i:i+requested]
            if len(selection) == requested:
                return selection

    # Else try all combinations across floors
    flat_rooms = []
    for floor, rooms in hotel_rooms.items():
        for r in rooms:
            if not r['booked']:
                flat_rooms.append(r['room'])

    flat_rooms.sort()
    for i in range(len(flat_rooms) - requested + 1):
        candidate = flat_rooms[i:i+requested]
        time = calculate_travel_time(candidate)
        if time < best_time:
            best_time = time
            best_choice = candidate

    return best_choice

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/book', methods=['POST'])
def book():
    data = request.json
    count = int(data.get('count', 1))
    if count < 1 or count > 5:
        return jsonify({'status': 'error', 'message': 'Invalid room count (1–5)'}), 400

    rooms_to_book = find_best_rooms(count)
    if not rooms_to_book:
        return jsonify({'status': 'fail', 'message': 'Not enough rooms available'}), 200

    # Mark rooms as booked
    for room_no in rooms_to_book:
        floor = room_no // 100 if room_no < 1000 else 10
        for r in hotel_rooms[floor]:
            if r['room'] == room_no:
                r['booked'] = True

    return jsonify({'status': 'success', 'booked_rooms': rooms_to_book})

@app.route('/randomize', methods=['POST'])
def randomize():
    initialize_rooms()
    for floor, rooms in hotel_rooms.items():
        for r in rooms:
            r['booked'] = random.random() < 0.3  # 30% chance room is booked
    return jsonify({'status': 'success'})

@app.route('/reset', methods=['POST'])
def reset():
    initialize_rooms()
    return jsonify({'status': 'success'})

@app.route('/status', methods=['GET'])
def status():
    return jsonify(hotel_rooms)

if __name__ == '__main__':
    app.run(debug=True)
