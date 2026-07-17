# AppointMate

## Overview
AppointMate is a healthcare appointment management system that makes it easy for patients to book doctor appointments and diagnostic tests, view current appointments, track prescriptions, and manage their profile from a single web interface.

The application includes a FastAPI backend with SQLAlchemy, JWT authentication, and a static frontend served directly from the backend.

## Features
- Patient registration and login
- JWT-based authentication for secure session handling
- Book doctor appointments and diagnostic tests
- Prevent overlapping appointments using unique time slot enforcement
- Patient dashboard for upcoming appointments, tests, and prescriptions
- Doctor dashboard for appointment management
- Admin support for managing doctors and users
- Static frontend pages served by FastAPI
- Legacy front-end code included in `legacy-frontend`

## Technology Stack
- Backend: Python, FastAPI, SQLAlchemy, Pydantic, python-dotenv
- Authentication: JWT, OAuth2 password grant, bcrypt password hashing
- Frontend: HTML5, CSS3, JavaScript (ES6)
- Database: Relational database configured via `db_url` environment variable

## Getting Started
### 1. Clone the repository
```bash
git clone https://github.com/yourusername/AppointMate.git
cd AppointMate
```

### 2. Create and activate a Python virtual environment
```bash
python -m venv ev
ev\Scripts\activate
```

### 3. Install dependencies
```bash
pip install fastapi uvicorn sqlalchemy python-dotenv python-jose passlib[bcrypt]
```

### 4. Configure environment variables
Create a `.env` file in the repository root or in the `backend/` folder with values like:
```env
DB_URL=mysql+pymysql://user:password@localhost/appointmate
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 5. Run database migration / schema update
```bash
python backend/database_migration.py
```

### 6. Start the application
```bash
cd backend
uvicorn main:app --reload
```

Open the app at `http://127.0.0.1:8000`.

## API Routes
- `POST /api/v1/signup` — create a new user
- `POST /api/v1/login` — authenticate and receive an access token
- `GET /api/v1/dashboard` — patient dashboard data
- `POST /api/v1/bookAppointment/{doc_id}` — book a doctor appointment
- `POST /api/v1/bookTest/{doc_id}` — book a diagnostic test
- `GET /api/v1/history` — appointment history
- `GET /api/v1/doctors` — list doctors and availability

## Notes
- Static frontend pages are served by FastAPI from the `frontend/` directory.
- The backend includes JWT authentication and uses protected routes for patient-specific dashboard data.
- A default admin user may be created by the migration script with email `admin@hospital.com` and password `admin123`.

## Contributors
- Shreeya Satav (Collaborated for the legacy-frontend)

