from fastapi import FastAPI
from fastapi.responses import FileResponse, RedirectResponse
from routes.routes import router
import routes.appointments
import routes.login_signup
import routes.patient
from fastapi.middleware.cors import CORSMiddleware

import routes.doctors
import routes.admin
import routes.doctors_dashboard
from fastapi.staticfiles import StaticFiles
import os
from pathlib import Path

version='v1'
app=FastAPI(
    title="Appointmate",
    description='AppointMate Healthcare System',
    version=version,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten this later for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router,prefix=f"/api/{version}/dashboard",tags=['dashboard'])
app.include_router(routes.appointments.router,prefix=f"/api/{version}",tags=['crud'])
app.include_router(routes.login_signup.router,prefix=f"/api/{version}",tags=['Login'])
app.include_router(routes.patient.router,prefix=f"/api/{version}")
app.include_router(routes.doctors.router,prefix=f"/api/{version}")
app.include_router(routes.admin.router,prefix=f"/api/{version}")
app.include_router(routes.doctors_dashboard.router,prefix=f"/api/{version}")

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR.parent / "frontend"

# Serve individual HTML pages explicitly so they load without conflicts
HTML_PAGES = [
    "index", "login", "signup", "profile", "dashboard",
    "book", "done", "doctor_dashboard", "admin_dashboard"
]

@app.get("/")
def serve_root():
    return FileResponse(str(FRONTEND_DIR / "index.html"))

for _page in HTML_PAGES:
    _html_path = str(FRONTEND_DIR / f"{_page}.html")
    def _make_handler(path):
        def handler():
            return FileResponse(path)
        return handler
    app.get(f"/{_page}.html")(_make_handler(_html_path))

# Serve static assets (CSS, JS, images)
app.mount("/", StaticFiles(directory=str(FRONTEND_DIR)), name="static")