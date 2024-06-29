# Project Management System (PMS)
This project is a comprehensive Project Management System built with Django. It supports both template-based views and REST API-based interactions. Users can manage projects, assign tasks, and track progress with ease. The system includes authentication, user management, and detailed API documentation using Swagger.

## Features
- User authentication and authorization
- Project creation and management
- Task assignment and progress tracking
- REST API support with full CRUD operations
- API documentation with Swagger and ReDoc


## Getting Started

### Prerequisites
- Python 3.12
- Django 5.0.6

### Installation

### 1. Clone the repository

   ```bash
   git clone https://github.com/emoncse/Project-Management
   cd Project-Management
   ```

### 2. Create a virtual environment
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

### 3. Install dependencies
   ```bash
    pip install -r requirements.txt
  ```


### 4. Apply migrations
```bash
    python manage.py makemigrations
    python manage.py migrate
```    

### 5. Create a superuser
```bash
    python manage.py createsuperuser
 ```

### 6. Run the application
```bash
    python manage.py runserver 127.0.0.1:8000
```

### 7. Access the application
```angular2html
    http://127.0.0.1:8000
```

## Template-Based Usage
- Access the application at http://127.0.0.1:8000/.
- Use the following endpoints for template-based views:

* ```/accounts/signup/ - User signup ```
* ```/accounts/login/ - User login ```
* ```/ - User dashboard ```
* ```/create_project/ - Create a new project ```
* ```/project/<int:pk>/ - View project details ```
* ```/project/<int:pk>/create_task/ - Create a task within a project ```
* ```/task/<int:pk>/update_progress/ - Update task progress ```
* ```/user_list/ - List all users ```
* ```/create_user/ - Create a new user ```


## REST API Usage
* Use the following API endpoints:

## ```/api/users/``` - User API endpoints
* ```GET /api/users/``` - User API endpoints
* ```POST /api/users/``` - Create a user
* ```GET /api/users/{id}/``` - Retrieve a user
* ```PUT /api/users/{id}/``` - Update a user
* ```DELETE /api/users/{id}/``` - Delete a user

## ```/api/projects/``` - Project API endpoints
* ```GET /api/projects/``` - List projects
* ```POST /api/projects/``` - Create a project
* ```GET /api/projects/{id}/``` - Retrieve a project
* ```PUT /api/projects/{id}/``` - Update a project
* ```DELETE /api/projects/{id}/``` - Delete a project

## ```/api/tasks/``` - Task API endpoints
* ```GET /api/tasks/``` - List tasks
* ```POST /api/tasks/``` - Create a task
* ```GET /api/tasks/{id}/``` - Retrieve a task
* ```PUT /api/tasks/{id}/``` - Update a task
* ```DELETE /api/tasks/{id}/``` - Delete a task

## Access the API Documentation
- Swagger: `http://127.0.0.1:8000/api/schema/swagger-ui/`
- ReDoc: `http://127.0.0.1:8000/api/schema/redoc/`

### Project Permissions
- Project Creator: Can create, update, and delete projects and tasks.
- Task Assignee: Can update the progress of assigned tasks.
- Admin: Can view and manage all projects and tasks.

## For Login with Github
- Create a Github OAuth App
- Add the Client ID and Client Secret to the admin panel under the `Social Applications` section.
- Add the redirect URL to the Github OAuth App settings.
- Also can be added to the setting file and env file based on environment setting.
- After adding the Client ID and Client Secret, the user can log in with Github.
- The user will be redirected to the Github login page and then back to the application.
- The github login is partially implemented. The user can log in with Github but the user data is not saved in the database.

### Thank you.