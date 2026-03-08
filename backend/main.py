from fastapi import FastAPI
from routes.routes import router
import routes.appointments

version='v1'
app=FastAPI(
    title="Appointmate",
    description='hai kuch toh',
    version=version,    
)

app.include_router(router,prefix=f"/api/{version}/dashboard",tags=['doctor'])
app.include_router(routes.appointments.router,prefix=f"/api/{version}/dashboard")