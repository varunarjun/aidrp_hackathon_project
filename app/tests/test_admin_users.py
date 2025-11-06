import os
import requests

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")
ADMIN_JWT = os.getenv("ADMIN_JWT", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NjI0Nzk4MDUsInN1YiI6ImFkbWluQGV4YW1wbGUuY29tIn0.vrix6WafRukZH8ztuBLWkB7DPkyIdS-C4l7iVVX7xfk")
HEADERS = {"Authorization": f"Bearer {ADMIN_JWT}"} if ADMIN_JWT else {}

# Use correct admin endpoints: /admin/users
def update_user(user_id: int, new_data: dict):
    url = f"{BASE_URL}/admin/admin/users/{user_id}"  # <-- fixed URL
    resp = requests.put(url, json=new_data, headers=HEADERS)
    print(f"\nPUT {url} -> Status: {resp.status_code}")
    _print_response(resp)

def delete_user(user_id: int):
    url = f"{BASE_URL}/admin/admin/users/{user_id}"  # <-- fixed URL
    resp = requests.delete(url, headers=HEADERS)
    print(f"\nDELETE {url} -> Status: {resp.status_code}")
    _print_response(resp)

def list_users():
    url = f"{BASE_URL}/admin/admin/users"  # <-- fixed URL
    resp = requests.get(url, headers=HEADERS)
    print(f"\nGET {url} -> Status: {resp.status_code}")
    _print_response(resp)

def _print_response(resp: requests.Response):
    try:
        print("Response JSON:", resp.json())
    except ValueError:
        print("Response text:", resp.text)

def main():
    # Example usage - change IDs and payloads as needed.
    print("Running admin users tests against:", BASE_URL)
    # list all users
    list_users()

    # Uncomment to run update/delete examples (adjust IDs)
    # update_data = {"role": "mentor", "is_active": True}
    # update_user(user_id=2, new_data=update_data)
    # delete_user(user_id=3)

if __name__ == "__main__":
    main()