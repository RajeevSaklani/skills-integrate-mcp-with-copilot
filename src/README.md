# Mergington High School Activities API

A super simple FastAPI application that allows students to view and sign up for extracurricular activities.

## Features

- View all available extracurricular activities
- View activity participants and remaining capacity
- Teachers can sign up or unregister students after logging in

## Getting Started

1. Install the dependencies:

   ```
   pip install -r requirements.txt
   ```

2. Add a teacher account. The command prompts for a password and stores only a salted hash in the local, Git-ignored `src/teachers.json` file. Run it again with the same username to reset that password.

   ```
   python src/manage_teachers.py teacher
   ```

3. Start the application from the repository root:

   ```
   python -m uvicorn src.app:app --host 0.0.0.0 --port 8000
   ```

4. Open your browser and go to:
   - API documentation: http://localhost:8000/docs
   - Alternative documentation: http://localhost:8000/redoc
   - Activities page: http://localhost:8000/

Teacher credentials are kept in browser memory and cleared on logout or page reload. The API uses HTTP Basic authentication for registration changes; use HTTPS before exposing the application beyond local development.

## API Endpoints

| Method | Endpoint                                                          | Description                                                         |
| ------ | ----------------------------------------------------------------- | ------------------------------------------------------------------- |
| GET    | `/activities`                                                     | Get all activities with their details and current participant count |
| POST   | `/auth/login`                                                      | Verify teacher credentials using HTTP Basic authentication         |
| POST   | `/activities/{activity_name}/signup?email=student@mergington.edu` | Sign up for an activity                                             |
| DELETE | `/activities/{activity_name}/unregister?email=student@mergington.edu` | Unregister a student from an activity                              |

Signup and unregister endpoints require valid teacher credentials. Activity and participant lists remain publicly viewable.

## Data Model

The application uses a simple data model with meaningful identifiers:

1. **Activities** - Uses activity name as identifier:

   - Description
   - Schedule
   - Maximum number of participants allowed
   - List of student emails who are signed up

2. **Students** - Uses email as identifier:
   - Name
   - Grade level

All data is stored in memory, which means data will be reset when the server restarts.
