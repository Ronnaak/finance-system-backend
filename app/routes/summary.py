from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import crud

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/summary/income", tags=["Summary"], description="Returns the total income recorded for the current user.")
def total_income(db: Session = Depends(get_db)):
    return {"total_income": crud.get_total_income(db)}

@router.get("/summary/expenses", tags=["Summary"], description="Returns the total expenses recorded for the current user.")
def total_expenses(db: Session = Depends(get_db)):
    return {"total_expenses": crud.get_total_expenses(db)}

@router.get("/summary/balance", tags=["Summary"], description="Shows the net balance calculated as total income minus total expenses.")
def balance(db: Session = Depends(get_db)):
    return {"balance": crud.get_balance(db)}

@router.get("/summary/category-breakdown", tags=["Summary"], description="Provides a breakdown of income and expenses grouped by category for better analysis.")
def category_breakdown(db: Session = Depends(get_db)):
    return {"category_breakdown": crud.get_category_breakdown(db)}

@router.get("/summary/monthly-totals", tags=["Summary"], description="Returns combined income and expenses for each month, useful for tracking monthly financial activity.")
def monthly_totals(db: Session = Depends(get_db)):
    return {"monthly_totals": crud.get_monthly_totals(db)}
