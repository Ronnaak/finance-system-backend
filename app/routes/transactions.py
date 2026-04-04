from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import SessionLocal
from app import crud, schemas, models
from app.users import role_required

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ------------------- Create Transaction -------------------
@router.post("/transactions/", response_model=schemas.Transaction , tags=["Transactions"])
def create_transaction(
    transaction: schemas.TransactionCreate,
    db: Session = Depends(get_db),
    user=Depends(role_required(["admin"]))
):
    try:
        return crud.create_transaction(db, transaction)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating transaction: {str(e)}")

# ------------------- Read Transaction by ID -------------------
@router.get("/transactions/{transaction_id}", response_model=schemas.Transaction, tags=["Transactions"])
def read_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    user=Depends(role_required(["viewer", "analyst", "admin"]))
):
    transaction = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction
# ------------------- Update Transaction -------------------
@router.put("/transactions/{transaction_id}", response_model=schemas.Transaction, tags=["Transactions"])
def update_transaction(
    transaction_id: int,
    updated_transaction: schemas.TransactionCreate,
    db: Session = Depends(get_db),
    user=Depends(role_required(["admin"]))
):
    transaction = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    # Update fields
    transaction.amount = updated_transaction.amount
    transaction.type = updated_transaction.type
    transaction.category = updated_transaction.category
    transaction.date = updated_transaction.date
    transaction.notes = updated_transaction.notes

    db.commit()
    db.refresh(transaction)
    return transaction


# ------------------- Delete Transaction -------------------
@router.delete("/transactions/{transaction_id}", tags=["Transactions"])
def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    user=Depends(role_required(["admin"]))
):
    transaction = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    db.delete(transaction)
    db.commit()
    return {"detail": "Transaction deleted successfully"}

# ------------------- Filter Transactions -------------------
@router.get("/transactions/", response_model=List[schemas.Transaction], tags=["Transactions"])
def filter_transactions(
    db: Session = Depends(get_db),
    user=Depends(role_required(["viewer", "analyst", "admin"])),
    type: Optional[str] = Query(None, description="Filter by type: income or expense"),
    category: Optional[str] = Query(None, description="Filter by category"),
    start_date: Optional[str] = Query(None, description="Filter from date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="Filter until date (YYYY-MM-DD)")
):
    query = db.query(models.Transaction)

    if type:
        query = query.filter(models.Transaction.type == type)
    if category:
        query = query.filter(models.Transaction.category == category)
    if start_date:
        query = query.filter(models.Transaction.date >= start_date)
    if end_date:
        query = query.filter(models.Transaction.date <= end_date)

    return query.all()
