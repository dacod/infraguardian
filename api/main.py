from fastapi import FastAPI
from api.routers import hosts

app = FastAPI(title="InfraGuardian API")

app.include_router(hosts.router)
