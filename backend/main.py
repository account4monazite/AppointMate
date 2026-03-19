from fastapi import FastAPI
from routes.routes import router
import routes.appointments
import routes.login_signup
import routes.patient
from fastapi.middleware.cors import CORSMiddleware


version='v1'
app=FastAPI(
    title="Appointmate",
    description='hai kuch toh',
    version=version,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten this later for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router,prefix=f"/api/{version}/dashboard",tags=['doctor'])
app.include_router(routes.appointments.router,prefix=f"/api/{version}",tags=['crud'])
app.include_router(routes.login_signup.router,prefix=f"/api/{version}")
app.include_router(routes.patient.router,prefix=f"/api/{version}")