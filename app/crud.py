from sqlalchemy.orm import Session
from sqlalchemy import func
from app import models, schemas

def get_transactions(db: Session):
    return db.query(models.Transaction).all()

def create_transaction(db: Session, transaction: schemas.TransactionCreate):
    db_transaction = models.Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction



#Summary Logic
def get_total_income(db: Session):
    return db.query(func.sum(models.Transaction.amount)).filter(models.Transaction.type == models.TransactionType.income).scalar() or 0

def get_total_expenses(db: Session):
    return db.query(func.sum(models.Transaction.amount)).filter(models.Transaction.type == models.TransactionType.expense).scalar() or 0

def get_balance(db: Session):
    income = get_total_income(db)
    expenses = get_total_expenses(db)
    return income - expenses

def get_category_breakdown(db: Session):
    results = db.query(models.Transaction.category, func.sum(models.Transaction.amount)).group_by(models.Transaction.category).all()
    return {category: total for category, total in results}

def get_monthly_totals(db: Session):
    results = db.query(
        func.strftime("%Y-%m", models.Transaction.date),
        func.sum(models.Transaction.amount)
    ).group_by(func.strftime("%Y-%m", models.Transaction.date)).all()
    return {month: total for month, total in results}
    
#User Handling
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserBase):
    db_user = models.User(username=user.username, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user