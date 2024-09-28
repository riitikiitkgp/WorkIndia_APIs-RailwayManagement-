import mysql.connector
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import threading, secrets

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'

jwt = JWTManager(app)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Ritik@12345",
    database="railway_system"
)
cursor = db.cursor()

ADMIN_API_KEY = secrets.token_hex(16)

# Helper function to run SQL query
def run_query(query, values=()):
    cursor.execute(query, values)
    db.commit()

# User registration
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data['username']
    password = data['password']
    role = data.get('role', 'user')
    run_query("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", (username, password, role))
    return jsonify(message="User registered successfully"), 201

# User login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()
    if user:
        access_token = create_access_token(identity={'id': user[0], 'username': user[1], 'role': user[3]})
        return jsonify(access_token=access_token), 200
    else:
        return jsonify(message="Invalid credentials"), 401

# Add a new train (Admin only)
@app.route('/add_train', methods=['POST'])
def add_train():
    if request.headers.get('X-API-KEY') != ADMIN_API_KEY:
        return jsonify(message="Unauthorized"), 403

    data = request.json
    train_name = data['train_name']
    source = data['source']
    destination = data['destination']
    total_seats = data['total_seats']
    run_query("INSERT INTO trains (train_name, source, destination, total_seats, available_seats) VALUES (%s, %s, %s, %s, %s)",
              (train_name, source, destination, total_seats, total_seats))
    return jsonify(message="Train added successfully"), 201

# Get seat availability between stations
@app.route('/availability', methods=['GET'])
def availability():
    source = request.args.get('source')
    destination = request.args.get('destination')
    cursor.execute("SELECT * FROM trains WHERE source=%s AND destination=%s", (source, destination))
    trains = cursor.fetchall()
    result = [{"train_name": train[1], "available_seats": train[5]} for train in trains]
    return jsonify(trains=result), 200

# Book a seat (User only, requires JWT authentication)
@app.route('/book_seat', methods=['POST'])
@jwt_required()
def book_seat():
    identity = get_jwt_identity()
    if identity['role'] != 'user':
        return jsonify(message="Only users can book seats"), 403

    data = request.json
    train_id = data['train_id']

    lock = threading.Lock()
    with lock:
        cursor.execute("SELECT available_seats FROM trains WHERE id=%s", (train_id,))
        train = cursor.fetchone()
        if train and train[0] > 0:
            run_query("UPDATE trains SET available_seats = available_seats - 1 WHERE id=%s", (train_id,))
            run_query("INSERT INTO bookings (user_id, train_id) VALUES (%s, %s)", (identity['id'], train_id))
            return jsonify(message="Seat booked successfully"), 200
        else:
            return jsonify(message="No seats available"), 400

# Get booking details (User only, requires JWT authentication)
@app.route('/booking_details', methods=['GET'])
@jwt_required()
def booking_details():
    identity = get_jwt_identity()
    cursor.execute("SELECT * FROM bookings WHERE user_id=%s", (identity['id'],))
    bookings = cursor.fetchall()
    result = [{"booking_id": booking[0], "train_id": booking[2], "booking_time": booking[3]} for booking in bookings]
    return jsonify(bookings=result), 200

if __name__ == '__main__':
    app.run(debug=True)
