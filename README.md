# SCM Project (Shipment Management System)

This project is a **Shipment Management System** built with **FastAPI** for the backend, **MongoDB** for the database, and uses **JWT** for authentication. The system allows users to manage and track shipments and devices, and also includes role-based authorization.

## Table of Contents
- [Features](#features)
- [Technologies](#technologies)
- [Installation Instructions](#installation-instructions)
  - [Prerequisites](#prerequisites)
  - [Setup](#setup)
  - [Environment Variables](#environment-variables)
  - [Running the Project](#running-the-project)
  - [Testing](#testing)
- [Usage](#usage)
- [License](#license)

## Features
- **User Authentication**: User signup and login with JWT-based authentication.
- **Role-Based Access Control**: Admin and user roles with appropriate permissions.
- **Shipment Management**: Create and view shipments.
- **Device Data**: Store and retrieve IoT device sensor data.
- **Frontend**: Static frontend for user interaction.

## Technologies
- **FastAPI** - Web framework for building APIs.
- **Uvicorn** - ASGI server for running FastAPI applications.
- **MongoDB** - NoSQL database to store user and shipment data.
- **JWT** - For user authentication.
- **Kafka** - Messaging service for communication (if needed).
- **Pydantic** - Data validation and settings management.
- **python-dotenv** - For loading environment variables.

## Installation Instructions

### Prerequisites
1. Install **Python 3.8+**.
2. Install **MongoDB** (or use a MongoDB cloud service like Atlas).
3. Set up **Kafka** if you plan to use it.

### Setup

Clone this repository to your local machine:

```bash
git clone https://github.com/your-username/scm-project.git
cd scm-project


Create a Virtual Environment and Activate It
Windows:

bash
Copy code
python -m venv venv
.\venv\Scripts\activate
Mac/Linux:

bash
Copy code
python3 -m venv venv
source venv/bin/activate
Environment Variables
Create a .env file in the root directory and add the following:

ini
Copy code
# MongoDB URI (for local MongoDB or Atlas connection)
MONGODB_URI=mongodb+srv://<your-username>:<your-password>@cluster0.mongodb.net/<your-db-name>?retryWrites=true&w=majority

# JWT Secret Key (Replace with your own secret key)
JWT_SECRET_KEY=your_jwt_secret_key
Make sure to replace the placeholders with your actual MongoDB URI and JWT secret key.

Install Dependencies
Install the required packages by running:

bash
Copy code
pip install -r requirements.txt
This will install the necessary dependencies for your project.

Running the Project
To run the backend server, use the following command:

bash
Copy code
uvicorn main:app --reload
This will start the server on http://127.0.0.1:8000.

The frontend files are served from the /frontend directory.

Testing
Unit Tests: You can write and run unit tests using any test framework like pytest.

API Endpoints: You can use tools like Postman or curl to test the API endpoints.

Usage
Sign Up: You can create a new user by sending a POST request to /auth/signup.

Login: Use the login form to authenticate the user and obtain a JWT token. The token is stored as an HTTP-only cookie.

Create Shipment: Admins can create new shipments by submitting a POST request to /shipment/create_shipment.

View Shipments: You can view all shipments by visiting /shipment/all_ships.

Device Data: Access device sensor data at /device/device_data.

License
This project is licensed under the MIT License - see the LICENSE file for details.

API Endpoints
Authentication Routes
POST /auth/signup - Sign up a new user.

POST /auth/login - Login and receive a JWT token.

POST /auth/renew_token - Renew the JWT token.

GET /auth/logout - Logout and delete the JWT token cookie.

Shipment Routes
POST /shipment/create_shipment - Create a new shipment.

GET /shipment/all_ships - Retrieve all shipments.

GET /shipment/get_shipment/{shipment_id} - Get details of a specific shipment.

GET /shipment/search_shipments - Search shipments based on the logged-in user.

Device Routes
GET /device/device_data - Retrieve the latest sensor data from IoT devices.

Development Notes
MongoDB: MongoDB stores user data, shipment details, and sensor readings.

JWT Authentication: User authentication is managed via JWT tokens. Tokens are set in cookies to manage user sessions.

Role-Based Access: Admin and user roles are used for controlling access to certain routes.

Note: Make sure to change the <your-username>, <your-password>, and <your-db-name> in the MongoDB URI and replace your_jwt_secret_key with your own secret key for security purposes.

Troubleshooting
Issue with MongoDB Connection: Ensure your MongoDB URI in the .env file is correct, especially if you are using MongoDB Atlas. Make sure your IP is whitelisted in the MongoDB Atlas dashboard.

JWT Token Issues: If you encounter issues with JWT tokens, ensure that your JWT_SECRET_KEY is correctly set in the .env file and the JWT token hasn't expired.

