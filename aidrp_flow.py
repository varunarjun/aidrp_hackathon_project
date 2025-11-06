import requests

# -----------------------------
# Config
# -----------------------------
BASE_URL = "http://127.0.0.1:8000"
USER_EMAIL = "testuser@example.com"
USER_PASSWORD = "Test123!"
ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = "Admin123!"
COURSE_ID = 1  # ID of course to enroll in

# -----------------------------
# Helper function to login and get JWT
# -----------------------------
def login(email, password):
    url = f"{BASE_URL}/auth/token"
    data = {
        "grant_type": "password",
        "username": email,
        "password": password,
        "scope": "",
        "client_id": "",
        "client_secret": ""
    }
    response = requests.post(url, data=data)
    response.raise_for_status()
    token = response.json()["access_token"]
    return token

# -----------------------------
# Enroll in a course
# -----------------------------
def enroll_course(user_token, course_id):
    url = f"{BASE_URL}/courses/courses/{course_id}/enroll"
    headers = {"Authorization": f"Bearer {user_token}"}
    response = requests.post(url, headers=headers)
    if response.status_code == 400 and "Already enrolled" in response.text:
        print(f"Already enrolled in course {course_id}")
        return
    response.raise_for_status()
    print(f"Enrolled in course {course_id}: {response.json()}")

# -----------------------------
# Get enrolled courses
# -----------------------------
def get_enrolled_courses(user_token):
    url = f"{BASE_URL}/courses/courses/enrolled"
    headers = {"Authorization": f"Bearer {user_token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    print("Enrolled Courses:")
    for course in data.get("enrolled_courses", []):
        print(f"- {course['title']} ({course['description']})")
    return data

# -----------------------------
# Send notification (Admin)
# -----------------------------
def send_notification(admin_token, recipient_email, title, message):
    url = f"{BASE_URL}/notifications/notifications/"
    headers = {"Authorization": f"Bearer {admin_token}", "Content-Type": "application/json"}
    payload = {
        "title": title,
        "message": message,
        "recipient": recipient_email
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    print("Notification sent:", response.json())

# -----------------------------
# Main Flow
# -----------------------------
if __name__ == "__main__":
    # 1️⃣ Login as user
    user_token = login(USER_EMAIL, USER_PASSWORD)
    print("User JWT:", user_token)

    # 2️⃣ Enroll in course
    enroll_course(user_token, COURSE_ID)

    # 3️⃣ Get enrolled courses
    enrolled = get_enrolled_courses(user_token)

    # 4️⃣ Login as admin to send notification
    admin_token = login(ADMIN_EMAIL, ADMIN_PASSWORD)
    send_notification(
        admin_token,
        recipient_email=USER_EMAIL,
        title="Course Enrollment Open",
        message=f"You are now enrolled in course ID {COURSE_ID}"
    )
