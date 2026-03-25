from sqlalchemy.orm import declarative_base , relationship
from sqlalchemy import Integer , String , Boolean,Column,ForeignKey
Base = declarative_base()

class ListItem(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True , index=True)
    title = Column(String)
    description = Column(String)
    is_completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User",back_populates="list_items")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True , index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    list_items = relationship("ListItem",back_populates="user")

    
