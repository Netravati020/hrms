# from database import Base, engine
# from sqlalchemy.orm import Session
# from sqlalchemy import schema
# from sqlalchemy.schema import EmployeesBase, BaseModel,EmployeecreateSchema
# # from models import Employee
# import models
#
#
#
# def get_items(db: Session,  limit: int = 100):
#     return db.query(models.Employee).limit(limit).all()
#
#
# print("created database")
#
# Base.metadata.create_all(engine)
#
# def create_user_item(db: Session, employees: schema.EmployeecreateSchema):
#     db_item = models.Employee(**employees.dict())
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item

# from fastapi import FastAPI, Depends, status, HTTPException
# from fastapi.security import OAuth2PasswordBearer
# from index import verify_token
#
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
#
#
# def get_current_user(data: str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     return verify_token(data, credentials_exception)