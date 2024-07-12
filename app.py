from flask import Flask, request, jsonify, render_template, redirect, url_for
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import math
import time  # Required for simulating wait time
import random

app = Flask(__name__)

# Helper function to calculate distance using Haversine formula
def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat1 - lat2
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371.0  # Radius of the Earth in kilometers
    return c * r

# Function to calculate toll amount based on distance and vehicle type
def calculate_toll(distance_km, vehicle_type):
    rates = {
        'car': {'base_rate': 2.0, 'per_km_rate': 1.5},
        'truck': {'base_rate': 5.0, 'per_km_rate': 2.0},
        'motorcycle': {'base_rate': 0.0, 'per_km_rate': 0.0},
        'heavy goods carrier': {'base_rate': 5.5, 'per_km_rate': 2.5},
    }
    

    if vehicle_type not in rates:
        raise ValueError(f"Invalid vehicle type: {vehicle_type}")
    
    rate = rates[vehicle_type]
    return rate['base_rate'] + (rate['per_km_rate'] * distance_km)

# Function to fetch coordinates of a city using geopy
def get_coordinates(city, retries=3):
    geolocator = Nominatim(user_agent="city_coordinates_locator")
    for _ in range(retries):
        try:
            location = geolocator.geocode(city, timeout=10)
            if location:
                return (location.latitude, location.longitude)
        except (GeocoderTimedOut, GeocoderServiceError) as e:
            print(f"Geocoding service error: {e}. Retrying...")
    raise ValueError(f"City '{city}' not found or geocoding failed after {retries} attempts.")

# Generate OTP function
def generate_otp():
    return ''.join(random.choices('0123456789', k=6))

# Render the index page
@app.route('/')
def index():
    return render_template('index.html')

# Calculate toll amount based on POST request data
@app.route('/calculate_toll', methods=['POST'])
def calculate_toll_route():
    data = request.get_json()
    start_city = data.get('start_city')
    end_city = data.get('end_city')
    vehicle_type = data.get('vehicle_type')
    vehicle_number = data.get('vehicle_number')

    if not start_city or not end_city or not vehicle_type or not vehicle_number:
        return jsonify({'error': 'Start city, end city, vehicle type, and vehicle number are required'}), 400
    
    if vehicle_type not in ['car', 'truck', 'motorcycle', 'heavy goods carrier']:
        return jsonify({'error': f'Invalid vehicle type: {vehicle_type}'}), 400

    try:
        start_coordinates = get_coordinates(start_city)
        end_coordinates = get_coordinates(end_city)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

    distance = haversine(start_coordinates[1], start_coordinates[0], end_coordinates[1], end_coordinates[0])
    try:
        if distance>50:
         toll_amount = calculate_toll(distance, vehicle_type)
        else:
         toll_amount=0
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

    return jsonify({
        'distance': distance,
        'toll_amount': toll_amount
    })

# Render payment options page
@app.route('/payment_options')
def payment_options():
    return render_template('payment_options.html')

# Render UPI payment page
@app.route('/upi_payment')
def upi_payment():
    return render_template('upi_payment.html')

# Handle UPI payment submission
@app.route('/submit_upi_payment', methods=['POST'])
def submit_upi_payment():
    data = request.get_json()
    upi_id = data.get('upi_id')

    if not upi_id:
        return jsonify({'error': 'UPI ID is required'}), 400

    # Here you would handle the UPI payment processing logic
    # For simplicity, we'll just return a success message
    # Simulate processing time
    time.sleep(4 * 60)  # Simulate 4 minutes wait

    return jsonify({'message': 'Payment successful!'}), 200

# Render bank payment page
@app.route('/bank_payment')
def bank_payment():
    return render_template('bank_payment.html')

# Handle bank payment submission and OTP generation
@app.route('/submit_bank_payment', methods=['POST'])
def submit_bank_payment():
    account_holder_name = request.form.get('account_holder_name')
    bank_name = request.form.get('bank_name')
    account_number = request.form.get('account_number')
    ifsc_number = request.form.get('ifsc_number')

    if not account_holder_name or not bank_name or not account_number or not ifsc_number:
        return jsonify({'error': 'All fields are required'}), 400

    # Generate OTP and store it temporarily
    otp = generate_otp()
    # Store OTP temporarily in session or database
    # For simplicity, we'll pass it as JSON response
    return jsonify({'otp': otp}), 200

# Render bank OTP verification page
@app.route('/bank_otp')
def bank_otp():
    return render_template('bank_otp.html')

# Handle OTP verification for bank payment
@app.route('/verify_bank_payment_otp', methods=['POST'])
def verify_bank_payment_otp():
    data = request.get_json()
    otp_entered = data.get('otp')
    expected_otp = data.get('expected_otp')

    if not otp_entered:
        return jsonify({'error': 'OTP is required'}), 400

    if otp_entered == expected_otp:
        return jsonify({'message': 'Payment successful!'}), 200
    else:
        return jsonify({'error': 'Entered OTP is incorrect'}), 400

# Render card payment page
@app.route('/card_payment')
def card_payment():
    return render_template('card_payment.html')

# Handle card payment submission
@app.route('/submit_card_payment', methods=['POST'])
def submit_card_payment():
    card_number = request.form.get('card_number')
    card_holder_name = request.form.get('card_holder_name')
    expiry_date = request.form.get('expiry_date')
    cvv = request.form.get('cvv')

    if not card_number or not card_holder_name or not expiry_date or not cvv:
        return jsonify({'error': 'All fields are required'}), 400

    # Here you would handle the card payment processing logic
    # For simplicity, we'll just return a success message
    return jsonify({'message': 'Payment successful!'}), 200

if __name__ == '__main__':
    app.run(debug=True)
