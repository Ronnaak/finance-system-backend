from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi import FastAPI
from app.routes import transactions, summary
from app import users


app = FastAPI(title="Finance System Backend",
    description="A Python-based finance tracking API with CRUD, summaries, and role-based access.",
    version="1.0.0")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": f"Unexpected error: {str(exc)}"}
    )
app.include_router(users.router)
app.include_router(transactions.router)
app.include_router(summary.router)
