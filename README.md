## Todo Web Application

### Overview
The Todo Web Application is a web application that allows users to create, edit, and delete tasks. It is built using FastAPI and Jinja.


## Usage

To use the Todo Web Application, follow these steps:
1) Install the required dependencies by running `pip install -r requirements.txt`
2) Run the docker-compose file by running `docker-compose up` to start the database
3) Run the application by running `uvicorn main:app --host localhost --port 8000 --reload`
4) Go to http://localhost:8000 in your browser

## Domain Model

 The Todo Web Application uses the following domain model:

### Todo
- title: The title of the task
- description: The description of the task
- complete: Whether the task is complete or not
- priority : The priority of the task
- owner_id: The id of the user who owns the task
### User
- email : The email of the user
- username: The username of the user
- first_name: The first name of the user
- last_name: The last name of the user
- hashed_password: The hashed password of the user
- is_active: Whether the user is active or not
- phone_numbers: The phone numbers of the user

## Features

- **User Authentication**: Secure login and registration with JWT.
- **Personalized Todo Lists**: Users manage their own private lists.
- **Todo Management**: Create, edit, delete, and mark items as complete/incomplete.


## API Endpoints and Responses

### **Authentication Routes**

#### **Login**
- **GET `/auth/`** → Returns login page (or redirects to `/todos` if logged in).
- **POST `/auth/`** → Authenticates user.
    - **302 Found** → Redirects to `/todos` on success.
    - **200 OK** → Returns login page with error message.

#### **Logout**
- **GET `/auth/logout`** → Logs out user and returns login page with success message.

#### **Register**
- **GET `/auth/register`** → Returns registration page (or redirects to `/todos` if logged in).
- **POST `/auth/register`** → Registers a new user.
    - **200 OK** → Redirects to login page on success.
    - **200 OK** → Returns register page with error message if invalid.

### **Todo List Routes**

#### **View Todos**
- **GET `/todos/`** → Returns user's todos (or redirects to `/auth/` if not logged in).

#### **Manage Todos**
- **GET `/todos/complete/{todo_id}`** → Toggles completion status of a todo, then redirects to `/todos/`.
- **GET `/todos/add-todo`** → Returns add-todo form (or redirects to `/auth/` if not logged in).
- **POST `/todos/add-todo`** → Creates a todo and redirects to `/todos/`.

#### **Edit Todos**
- **GET `/todos/edit-todo/{todo_id}`** → Returns edit form for a todo.
- **POST `/todos/edit-todo/{todo_id}`** → Updates a todo and redirects to `/todos/`.

#### **Delete Todo**
- **GET `/todos/delete-todo/{todo_id}`** → Deletes a todo and redirects to `/todos/`.

### **Error Handling**
- **404 Not Found** → `{"detail": "Todo Not Found!"}`
- **401 Unauthorized** → `{"user": "Not Authorized"}` or `{"todos": "Not Found!"}`
- **200 OK (Success)** → `{"status": 200, "transaction": "Successful"}`


## Technical Features

### **Backend Technologies**
- **FastAPI**: High-performance web framework for building APIs.
- **SQLAlchemy**: ORM for database interactions.
- **PostgreSQL**: Database management system (can be replaced as needed).
- **Dependency Injection**: Used for database sessions and authentication.
- **JWT (JSON Web Tokens)**: Secure authentication and user authorization.
- **bcrypt**: Password hashing for security.
- **OAuth2 with Password Flow**: Token-based authentication.

### **Frontend & Templates**
- **Jinja2**: Templating engine for rendering HTML.
- **HTML/CSS**: Used for frontend UI structure.
- **Starlette Templates & Responses**: For serving HTML responses.

### **User Authentication & Security**
- **OAuth2PasswordBearer**: Token-based authentication.
- **JWT Encoding & Decoding**: Secure token generation and validation.
- **Password Hashing**: `passlib.context.CryptContext` for secure password storage.
- **Session-Based Authentication**: Cookies used for session persistence.

### **Routing & Middleware**
- **APIRouter**: Modular API structuring.
- **Middleware for Authentication**: Ensures only authorized users access protected routes.
- **Redirect Responses**: Ensures correct authentication flow.

### **Database Management**
- **SQLAlchemy ORM**: Object-relational mapping for models.
- **Session Management**: Efficient database connections using FastAPI's dependency injection.

### **Task & Todo Management**
- **CRUD Operations**: Create, Read, Update, Delete functionality for todos.
- **Filtering**: Fetch todos specific to logged-in users.
- **Completion Status Updates**: Allows marking todos as complete/incomplete.

### **Error Handling**
- **Custom Exception Handling**: `HTTPException` for managing invalid requests.
- **404 Not Found & 401 Unauthorized**: Predefined error messages for better UX.

### **API Docs**
- **Interactive API Docs**: Swagger UI (`/docs`) and ReDoc (`/redoc`) auto-generated by FastAPI.

--------