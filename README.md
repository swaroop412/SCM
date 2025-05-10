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

