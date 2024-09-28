# Railway Management System

A simple railway management system built using Flask and MySQL, allowing users to check train availability, book seats, and manage user accounts. The system features role-based access control with distinct functionalities for admin and regular users.

## Features

- **User Registration**: Users can create accounts.
- **User Login**: Users can log in to their accounts using JWT authentication.
- **Admin Operations**: Admins can add new trains with source, destination, and seat availability.
- **Check Seat Availability**: Users can check the availability of seats between two stations.
- **Book Seats**: Users can book seats on available trains.
- **Booking Details**: Users can retrieve their booking details.

## Tech Stack

- **Backend Framework**: Flask
- **Database**: MySQL
- **Authentication**: JWT (JSON Web Tokens)

## API Endpoints

## User Registration

Endpoint: /register
Method: POST
Body:

{
    "username": "user123",
    "password": "password123"
}

## User Login
Endpoint: /login
Method: POST
Body:

{
    "username": "user123",
    "password": "password123"
}

## Add a New Train (Admin only)
Endpoint: /add_train

Method: POST

Headers:
{
    "X-API-KEY": "69f4ed8fcaa222e73ee887b1dbf704a8"
}

Body:
{
    "train_name": "Express Train",
    "source": "Station A",
    "destination": "Station B",
    "total_seats": 100
}

## Get Seat Availability

Endpoint: /availability

Method: GET

Query Parameters:
source: Station name
destination: Station name

## Book a Seat

Endpoint: /book_seat

Method: POST

Headers:
{
    "Authorization": "Bearer <token>"
}

Body:
{
    "train_id": 1
}

## Get Booking Details

Endpoint: /booking_details

Method: GET

Headers:
{
    "Authorization": "Bearer <token>"
}
