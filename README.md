🚀 AI Disaster Response and Prediction Platform (AIDRP) - Python Backend

Version: 0.1.0
Stack: Python, FastAPI, PostgreSQL, SQLAlchemy, JWT Auth, Pandas, Docker, Swagger/OpenAPI

🔹 Project Overview

The AI Disaster Response and Prediction Platform (AIDRP) is a backend service designed to help authorities and organizations predict disasters, manage incidents, allocate resources, and track courses/training for responders. This service provides REST APIs to handle:

User authentication and role management (Admin, Mentor, Student)

Course and content management

Incident reporting and tracking

Sensor data management

Notifications and daily/weekly reporting

AI-based resource allocation predictions

This backend can be integrated with a frontend dashboard for real-time disaster management.

🔹 Features & Endpoints
Health & Root
Method	Endpoint	Description
GET	/	API Root / Welcome message
GET	/status	Service Health Check
Authentication
Method	Endpoint	Description
POST	/auth/register	Register new users
POST	/auth/token	Login & get JWT token
GET	/auth/profile	Get current user profile
POST	/auth/logout	Logout user (invalidate session)
Courses & Modules
Method	Endpoint	Description
GET	/courses/courses/	List all courses
POST	/courses/courses/	Create a new course
POST	/courses/courses/{course_id}/modules	Add module to course
PUT	/courses/courses/{course_id}	Update course details
DELETE	/courses/courses/{course_id}	Delete course
POST	/courses/courses/{course_id}/enroll	Enroll a user in course
GET	/courses/courses/enrolled	Get courses user is enrolled in
Admin Users
Method	Endpoint	Description
GET	/admin/admin/users	List all users
PUT	/admin/admin/users/{user_id}	Update user info
DELETE	/admin/admin/users/{user_id}	Delete user
Notifications
Method	Endpoint	Description
GET	/admin/notifications/admin/notifications/	Get all notifications
POST	/admin/notifications/admin/notifications/	Create notification
DELETE	/admin/notifications/admin/notifications/{notification_id}	Delete notification
GET	/admin/notifications/admin/notifications/report/daily	Generate daily notification report
Incidents
Method	Endpoint	Description
GET	/incidents/incidents/	Get all incidents
POST	/incidents/incidents/	Create a new incident
GET	/incidents/incidents/{incident_id}	Get incident by ID
DELETE	/incidents/incidents/{incident_id}	Delete incident
Sensors
Method	Endpoint	Description
GET	/sensors/sensors/	Get all sensors
POST	/sensors/sensors/	Create a new sensor
GET	/sensors/sensors/{sensor_id}	Get sensor by ID
DELETE	/sensors/sensors/{sensor_id}	Delete sensor
Resource Allocation / AI Pipelines
Method	Endpoint	Description
GET	/allocation/allocation/predict?incident_type=&severity=	Predict required resources for an incident (AI-based)

Parameters:

incident_type (string, required) – Type of incident (e.g., fire, flood)

severity (integer, required) – Severity level of incident

Response: Dynamic prediction of required resources (ambulances, fire trucks, etc.).

🔹 Database Models

Users: Manage authentication, roles (Admin, Mentor, Student)

Courses & Modules: Tracks courses, modules, and enrollments

Notifications: Stores messages and generates reports

Incidents: Tracks disaster incidents reported

Sensors: Stores IoT sensor data for real-time monitoring

Resource Allocation: AI prediction for emergency response

🔹 Installation & Setup Instructions

Follow these steps to run the backend locally:

1️⃣ Clone the Repository
git clone https://github.com/varunarjun/aidrp_hackathon_project
cd aidrp-python

2️⃣ Create Virtual Environment
python -m venv venv
# Activate environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

3️⃣ Install Dependencies
pip install --upgrade pip
pip install -r requirements.txt

4️⃣ Setup Environment Variables

Create a .env file in the root:

# -------------------------
# MySQL Database Configuration
# -------------------------
MYSQL_USER=aidrp_user
MYSQL_PASSWORD=StrongPassword123!
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DB=aidrp_db

# Optional: Full SQLAlchemy URL (overrides above if set)
DATABASE_URL=mysql+pymysql://aidrp_user:StrongPassword123!@localhost:3306/aidrp_db

# -------------------------
# JWT / Authentication
# -------------------------
SECRET_KEY=THIS_IS_A_SECRET_CHANGE_ME
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# -------------------------
# Application Host & Port
# -------------------------
APP_HOST=0.0.0.0
APP_PORT=8000

# -------------------------
# SMTP / Email Settings
# -------------------------
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=your-email@example.com
SMTP_PASSWORD=your-email-password
FROM_EMAIL=your-email@example.com

DATABASE_URL=postgresql://username:password@localhost:5432/aidrp_db
SECRET_KEY=your_secret_jwt_key
ACCESS_TOKEN_EXPIRE_MINUTES=60

5️⃣ Initialize Database
# If using PostgreSQL
# Ensure database `aidrp_db` exists
python -m app.database
# or run migrations if using Alembic

6️⃣ Run the API Server
uvicorn app.main:app --reload


Server will run at: http://127.0.0.1:8000

7️⃣ API Documentation

Swagger UI: http://127.0.0.1:8000/docs

OpenAPI JSON: http://127.0.0.1:8000/openapi.json

🔹 Testing Endpoints

Use Postman or Swagger UI to test all endpoints. Example:

Login & Get JWT

POST /auth/token
Body:
{
  "username": "admin@example.com",
  "password": "password123"
}


Access Protected Route

GET /auth/profile
Headers:
Authorization: Bearer <JWT_TOKEN>

🔹 Optional: Docker Setup
# Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Build Docker image
docker build -t aidrp-backend .
# Run Docker container
docker run -p 8000:8000 aidrp-backend

🔹 Contributing / Notes

Ensure code is formatted with Black before commit.

Include .env.example for reference.

Write unit tests for new endpoints using PyTest.

Maintain standard FastAPI project structure.