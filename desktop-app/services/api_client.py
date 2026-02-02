import requests

API_BASE = "http://127.0.0.1:8000/api"

class ChemicalAPIClient:
    def __init__(self):
        self.access_token = None
        self.refresh_token = None

    def login(self, username, password):
        """Authenticates and stores JWT tokens."""
        url = f"{API_BASE}/token/"
        response = requests.post(url, json={"username": username, "password": password})
        
        if response.status_code == 200:
            data = response.json()
            self.access_token = data['access']
            self.refresh_token = data['refresh']
            print("Login successful!")
            return True
        else:
            print(f"Login failed: {response.status_code}")
            return False

    def get_headers(self):
        """Helper to generate auth headers."""
        if not self.access_token:
            return {}
        return {"Authorization": f"Bearer {self.access_token}"}

    def upload_csv(self, file_path):
        """Uploads a CSV file using the JWT token."""
        url = f"{API_BASE}/upload/"
        try:
            with open(file_path, 'rb') as f:
                files = {'file': f}
                response = requests.post(url, files=files, headers=self.get_headers())
                response.raise_for_status()
                return response.json()
        except requests.exceptions.HTTPError as e:
            return f"Upload error: {e.response.text}"

    def fetch_history(self):
        """Fetches history using the JWT token."""
        url = f"{API_BASE}/history/"
        try:
            response = requests.get(url, headers=self.get_headers())
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            return f"Fetch error: {e.response.text}"

# --- Example Usage ---
client = ChemicalAPIClient()

# 1. You MUST login first to get the token
if client.login("axara", "backend"):
    # 2. Now you can fetch data
    history = client.fetch_history()
    print(history)
    
    # 3. And upload files
    # result = client.upload_csv("data.csv")
    # print(result)