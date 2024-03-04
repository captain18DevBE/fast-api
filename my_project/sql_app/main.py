from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from sql_app import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


#Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


'''
HOME_WORK 9-12
'''

'''
API for database User
'''

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_users(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_email}", response_model=schemas.User)
def read_user(user_email: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db=db, email=user_email)
    
    return user
    


'''
API for database Item
'''

@app.post("/users/{user_id}/items/", response_model=schemas.Item)
async def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(user_id=user_id, item=item, db=db)
    

@app.get("/items/{item_id}", response_model=schemas.Item)
async def read_item(item_id: int, db: Session = Depends(get_db)):
    item = crud.get_item(item_id=item_id, db=db)
    return item    


'''
HOME_WORK 1-8
'''

@app.get('/v1/validate/{year}')
async def simple_route_v1_name(year: int):
    if year < 1900 or year > datetime.now().year:
        return f'The {year} is invalid!'
    return f'The {year} is valid!'


@app.get('/day_status/{year}/{month}/{day}')
async def simple_route_v1_calendar(year: int, month: int, day: int):
    
    try:
        if not (1 <= month <= 12):
            raise HTTPException(status_code=400, detail="The is not valid")
        if day > calendar.monthrange(year, month)[1]:
            raise HTTPException(status_code=400, detail="The day is not valid")
        
        weekday = calendar.weekday(year, month, day)
        if 0 <= weekday <= 4:
            return 'The day is a weekday'
        return 'The day is a weekend'
    
    except ValueError:
        raise HTTPException(status_code=400, detail="Value Error")
    
    