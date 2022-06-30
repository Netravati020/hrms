# from fastapi import APIRouter, Depends
# import schema
# import models
# from sqlalchemy.orm import Session
# from database import get_db
#
#
#
# router = APIRouter()
#
#
#
# @router.get('/employees', tags=['Employees'])
# def read_emp(db: Session = Depends(get_db)):
#     emp= db.query(models.Employee).all()
#     return emp