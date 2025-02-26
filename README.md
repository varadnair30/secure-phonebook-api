# Secure Phone Book REST API

## Overview

This project implements a secure Phone Book REST API using Python. The API ensures input validation using regular expressions and incorporates security features such as authentication, authorization, and logging. 

The project is submitted in two versions:
- **FastAPI Implementation**
- **Flask Implementation**

## Features

- **Phone Book Management**
  - List all contacts (`GET /PhoneBook/list`)
  - Add a contact (`POST /PhoneBook/add`)
  - Delete a contact by name (`PUT /PhoneBook/deleteByName`)
  - Delete a contact by phone number (`PUT /PhoneBook/deleteByNumber`)

- **Security**
  - Input validation using regular expressions
  - Authentication and authorization with role-based access
  - Audit logging of all key actions

- **Data Storage**
  - Persistence using SQLite (with an option to use other formats)
  - Secure parameterized queries to prevent SQL injection

- **Testing**
  - Automated security-focused unit tests
  - Postman collection provided for API testing

- **Deployment**
  - Dockerized for easy setup and testing
  - Includes necessary dependencies in Docker containers

## API Endpoints

| Method | Endpoint                   | Description |
|--------|----------------------------|-------------|
| `GET`  | `/PhoneBook/list`          | Retrieves all contacts |
| `POST` | `/PhoneBook/add`           | Adds a new contact (expects JSON input) |
| `PUT`  | `/PhoneBook/deleteByName`  | Deletes a contact by name |
| `PUT`  | `/PhoneBook/deleteByNumber`| Deletes a contact by phone number |

## Input Validation

- **Valid Names:**  
  - `Bruce Schneier`  
  - `Schneier, Bruce`  
  - `Schneier, Bruce Wayne`  
  - `O’Malley, John F.`  

- **Valid Phone Numbers:**  
  - `(703)111-2121`  
  - `+1(703)111-2121`  
  - `011 701 111 1234`  

Invalid inputs such as SQL injection attempts, scripts, or improperly formatted numbers will be rejected with a `400` status code.

## Setup and Installation

### Prerequisites
- Python 3.8+
- Docker
- FastAPI or Flask (depending on the implementation)

### Running with Docker
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/secure-phonebook-api.git
   cd secure-phonebook-api

2. Build and run the Docker container:
   ```sh
   docker-compose up --build

3. Access the API at:
   - FastAPI: http://localhost:8000/docs
   - Flask: http://localhost:5000

![image](https://github.com/user-attachments/assets/810ea206-e6a9-4601-a66b-b1a23e0d7289)

### Testing
Run unit tests with:

```sh
pytest tests/
