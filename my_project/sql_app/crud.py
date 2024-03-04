from sqlalchemy.orm import Session
from . import models, schemas


'''
CRUD for User model
'''

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 0):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_users(db: Session, user: schemas.UserCreate):
    fake_hashed_password =user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

'''
CRUD for Item model
'''

def get_items(db: Session, skip: int=0, limit: int=10):
    return db.query(models.Item).offset(skip).limit(limit).all()

def get_item(item_id: int, db: Session):
    return db.query(models.Item).filter(models.Item.id == item_id).first()
    

def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.model_dump(), owner_id=user_id)
    
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    
    return db_item
    
    