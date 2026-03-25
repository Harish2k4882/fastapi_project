from fastapi import FastAPI, Depends
from typing import List
from models import ListItem,UserCreate,ShowUser,ShowList,UserCreate,ShowItemWithUser
from data_base import SessionLocal, engine
import database_models
from sqlalchemy.orm import Session
from pwdlib import PasswordHash
database_models.Base.metadata.create_all(bind=engine)


from fastapi.middleware.cors import CORSMiddleware
pwd_context = PasswordHash.recommended()


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()
        
@app.get("/products",tags=['items'],response_model=List[ShowItemWithUser])
def get_all_products(db:Session = Depends(get_db)):
    from_db = db.query(database_models.ListItem).all()
    return from_db

@app.get("/product/{id}",tags=['items'])
def get_product(id:int,db:Session = Depends(get_db)):
    from_db = db.query(database_models.ListItem).filter(database_models.ListItem.id == id).first()
    if from_db:
        return from_db
    return "Item Not Found"

@app.post("/product/{user_id}",tags=['items'])

def add_product(item:ListItem,db:Session = Depends(get_db)):
    new_item = database_models.ListItem(id=item.id,title=item.title,description=item.description,is_completed=item.is_completed,user_id=1)
    db.add(new_item)
    db.commit()
    return "Item Added..."


@app.put("/product",tags=['items'])

def update_product(id:int,item:ListItem,db:Session = Depends(get_db)):
    update_item = db.query(database_models.ListItem).filter(database_models.ListItem.id == id).first()
    if update_item:
        update_item.id = item.id
        update_item.title = item.title
        update_item.description= item.description
        update_item.is_completed = item.is_completed
        db.commit()
        return "Updated Successfully...."
    else:
        return "Product Not Found"
@app.delete("/product",tags=['items'])
def delete_product(id:int,db:Session = Depends(get_db)):
    delete_item = db.query(database_models.ListItem).filter(database_models.ListItem.id == id).first()
    if delete_item:
        db.delete(delete_item)
        db.commit()
        return "Deleted Successfull...."
    else:
        return "Product Not Found"
    
@app.post("/user",tags=["users"])
def add_user(user:UserCreate, db:Session = Depends(get_db)):
    Passwordhashing = pwd_context.hash(user.password)
    new_user = database_models.User(
        name= user.username,
        email=user.email,
        password=Passwordhashing
    )
    db.add(new_user)
    db.commit()
    return "User Added..."
@app.get("/user/{id}",tags=["users"],response_model=ShowUser)
def get_user(id:int, db:Session = Depends(get_db)):
    get_user_from_db = db.query(database_models.User).filter(database_models.User.id == id).first()
    if get_user_from_db:
        return get_user_from_db
    return "User Not Found In Database..." 
@app.get("/users",tags=["users"])
def get_users(db:Session = Depends(get_db)):
    get_user_from_db = db.query(database_models.User).all()
    return get_user_from_db 
