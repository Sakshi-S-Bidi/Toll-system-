# Dynamic Toll System

This is a Flask-based web application that calculates toll amounts dynamically based on distance, vehicle type, and road usage. It uses the Haversine formula to calculate the distance between two cities and offers multiple payment options for toll payments.

## Features

- Calculate toll amounts based on distance and vehicle type.
- Fetch coordinates of cities using Geopy.
- Multiple payment options including UPI, bank transfer with OTP verification, and card payments.
- Dynamic rate adjustment for different vehicle types.

## Requirements

- Python 3.x
- Flask
- Geopy

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/dynamic-toll-system.git
    ```
2. Navigate to the project directory:
    ```bash
    cd dynamic-toll-system
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

1. Run the Flask application:
    ```bash
    python app.py
    ```
2. Open your web browser and go to `http://127.0.0.1:5000/` to access the application.

## Endpoints

### `GET /`

Renders the index page.

### `POST /calculate_toll`

Calculates the toll amount based on the provided start city, end city, and vehicle type.

**Request JSON Format:**
```json
{
    "start_city": "City A",
    "end_city": "City B",
    "vehicle_type": "car",
    "vehicle_number": "XYZ1234"
}
