# Todo Web Application

![Todo Web Application](https://github.com/omarhammad/todo_web/blob/main/static/todo/media/home.png)

---

## Table of Contents
- [Overview](#overview)
- [Key Features](#key-features)
- [Domain Model](#domain-model)
- [Technologies Used](#technologies-used)
- [Setup and Installation](#setup-and-installation)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Security and Authentication](#security-and-authentication)
- [Deployment](#deployment)
- [Contributors](#contributors)

---

## Overview
The Todo Web Application is a web application that allows users to create, edit, and delete tasks. It is built using FastAPI and Jinja.

## Key Features
- **User Authentication**: Secure login and registration with JWT.
- **Personalized Todo Lists**: Users manage their own private lists.
- **Todo Management**: Create, edit, delete, and mark items as complete/incomplete.

## Domain Model
### Todo
- `title`: The title of the task
- `description`: The description of the task
- `complete`: Whether the task is complete or not
- `priority`: The priority of the task
- `owner_id`: The ID of the user who owns the task

### User
- `email`: The email of the user
- `username`: The username of the user
- `first_name`: The first name of the user
- `last_name`: The last name of the user
- `hashed_password`: The hashed password of the user
- `is_active`: Whether the user is active or not
- `phone_numbers`: The phone numbers of the user

## Technologies Used
- **Backend**: FastAPI, SQLAlchemy, PostgreSQL
- **Security**: OAuth2, JWT, bcrypt
- **Frontend**: Jinja2, HTML, CSS
- **Deployment**: Docker, Google Cloud, Cloud SQL, SSL/TLS

## Setup and Installation
1. Activate the virtual environment: `source venv/bin/activate`
2. Install dependencies: `pip install -r requirements.txt`
3. Start the database: `docker-compose up`
4. Run the application: `uvicorn main:app --host localhost --port 8000 --reload`
5. Open [http://localhost:8000](http://localhost:8000) in your browser

## API Endpoints
### Authentication Routes
- **GET `/auth/`** → Returns login page (or redirects to `/todos` if logged in).
- **POST `/auth/`** → Authenticates user and redirects.
- **GET `/auth/logout`** → Logs out user.
- **GET `/auth/register`** → Returns registration page.
- **POST `/auth/register`** → Registers a new user.

### Todo List Routes
- **GET `/todos/`** → Returns user's todos.
- **GET `/todos/complete/{todo_id}`** → Toggles completion status.
- **GET `/todos/add-todo`** → Returns add-todo form.
- **POST `/todos/add-todo`** → Creates a new todo.
- **GET `/todos/edit-todo/{todo_id}`** → Returns edit form.
- **POST `/todos/edit-todo/{todo_id}`** → Updates a todo.
- **GET `/todos/delete-todo/{todo_id}`** → Deletes a todo.

## Testing
- **API Testing**: Use tools like Postman or Curl to interact with the API.

## Security and Authentication
- **OAuth2PasswordBearer** for token-based authentication
- **JWT Encoding & Decoding** for secure session management
- **bcrypt** for password hashing
- **Middleware for Authentication** ensures protected routes

## Deployment
- **Compute Engine**
  - Provision a Google Cloud VM to host the application and database.
  - Install Docker, apply security updates, and configure firewall rules.

- **Cloud SQL**
  - Create a PostgreSQL instance with a database and user.
  - Authorize the VM and initialize the schema.

- **Cloud Storage**
  - Create a storage bucket for static files with public access if needed.

- **VPC Networking**
  - Set up a dedicated VPC with a custom subnet.
  - Apply firewall rules for secure communication.

- **Domain & DNS**
  - Register a domain and configure Cloud DNS.
  - Update nameservers in the domain provider.

- **Application Deployment**
  - Use **Docker Compose** for container orchestration.
  - Set up SSL/TLS certificates and Cloud SQL proxy.
  - Build, push, and deploy the application.

## Contributors

👨‍💻 **Omar Yahya M Hammad**  
📧 Email: [omarhammad767@gmail.com](mailto:omarhammad767@gmail.com)

---
