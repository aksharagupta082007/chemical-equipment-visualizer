# ⚗️ Chemical Equipment Visualizer (Hybrid Suite) A professional-grade hybrid system for Chemical Engineers to upload, analyze, and visualize equipment telemetry. This project features a **Django REST API** secured with **JWT Authentication**, serving both a **React Web Dashboard** and a **PyQt5 Desktop Application**. --- ## 📂 Project Structure
text
.
├── backend/
│   ├── venv/                 # Virtual environment (ignored by Git)
│   ├── server/               # Django project root
│   │   ├── manage.py         # Entry point for backend
│   │   ├── server/           # Project settings & URLs
│   │   └── equipment/        # Main API App (Logic, Serializers, Views)
│   ├── media/uploads/        # Storage for uploaded CSV files
│   ├── db.sqlite3            # Database
│   └── requirements.txt      # Backend dependencies
│
├── desktop_app/              # PyQt5 Application (The tool you are editing)
│   ├── main_window.py        # Desktop Entry Point
│   ├── ui/                   # Custom UI & Charts
│   └── services/             # API Client & JWT Logic
│
└── frontend/                 # React Web Dashboard
    ├── src/                  # Components & API services
    └── package.json          # Web dependencies
--- ## ⚙️ Setup & Installation ### 1. Backend (Django REST API) The "brain" of the project. It handles authentication and data processing.
bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt

# Database Setup
cd server
python manage.py migrate
python manage.py createsuperuser  # Create your admin/login credentials

# Start Server
python manage.py runserver
### 2. Desktop Application (PyQt5) The specialized analytical tool for high-fidelity visualization.
bash
# Ensure virtual environment is active
cd desktop_app
pip install pyqt5 matplotlib requests pandas

# Launch the application
python main_window.py
*When prompted, log in using the **superuser** credentials created in Step 1.* ### 3. Web Dashboard (React) The remote monitoring portal. Requires **Node.js** installed.
bash
cd frontend
npm install
npm start
--- ## 📡 API Overview & Auth This project uses **JWT (JSON Web Tokens)** to secure data. Every request from the Desktop or Web app must include an Authorization: Bearer <token> header. | Endpoint | Method | Auth | Description | | --- | --- | --- | --- | | /api/token/ | POST | ❌ | Login to get JWT Tokens | | /api/upload/ | POST | ✅ | Upload CSV (Processes via Pandas) | | /api/history/ | GET | ✅ | Retrieve the last 5 datasets | **CSV Requirement:** Files must include columns for Type, Flowrate, Pressure, and Temperature. --- ## 🛠 Features & Capabilities * **Secure CSV Upload:** Authenticated-only access to prevent unauthorized data injection. * **Engineering Neon Theme:** Custom-styled PyQt5 and CSS interfaces optimized for readability. * **Data Persistence:** Files uploaded via the Desktop App are instantly available on the Web Dashboard history thanks to the unified Django backend. * **Real-time Analytics:** Automated calculation of average flow, pressure, and temperature upon upload. --- ## ✅ Project Status * [x] **Backend:** API and JWT Auth fully operational. * [x] **Desktop:** PyQt5 Frontend integrated with API authentication. * [x] **Web:** React Dashboard communicating with shared database. * [x] **Processing:** Automated Pandas-based CSV analysis. ---
