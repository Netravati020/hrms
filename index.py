
from typing import Optional, Union
import crud
from fastapi import FastAPI, Depends, status, HTTPException, Response, Request, Form, File, UploadFile, Cookie

from fastapi.encoders import jsonable_encoder
from passlib.context import CryptContext
from hashing import Hash
# from routers import ameer

from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from starlette.responses import JSONResponse

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



from sqlalchemy.orm import Session

import schema
import models
import hashing
from database import engine,Base,SessionLocal

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


models.Base.metadata.create_all(bind=engine)

# Inserting new employee
@app.post('/creat', status_code=status.HTTP_201_CREATED, tags=['Employees'])
def create_emp(request:schema.Employee, db:Session=Depends(get_db)):

    e=models.Employee(

                      # Name=request.Name,
                      # contact=request.contact,
                      # email=request.email,
                      # department=request.department,
                      # salary=request.salary
        unit_code=request.unit_code,
        category_code=request.category_code,
        employee_id=request.employee_id,
        name=request.name,
        gender=request.gender,
        relegion=request.relegion,
        relegion_description=request.relegion_description,
        nationality=request.nationality,
        factory_act_flag=request.factory_act_flag,
        designation_code=request.designation_code,
        class_of_employee=request.class_of_employee,
        weekly_off_day=request.weekly_off_day,
        direct_recruity_promotee=request.direct_recruity_promotee,
        section_code=request.section_code,
        dob=request.dob,
        initial_appointment_date=request.initial_appointment_date,
        date_of_regular=request.date_of_regular,
        date_of_last_increment_drawn=request.date_of_last_increment_drawn,
        date_of_medical_examination_done=request.date_of_medical_examination_done,
        basic_pay=request.basic_pay,
        protected_pay=request.protected_pay,
        grade_pay=request.grade_pay,
        special_pay=request.special_pay,
        family_planning_pay=request.family_planning_pay,
        telangana_incentive=request.telangana_incentive,
        graduation_increment=request.graduation_increment,
        equalisation_allowance=request.equalisation_allowance,
        special_allowance=request.special_allowance,
        special_allowance1=request.special_allowance1,
        father_spouse_name=request.father_spouse_name,
        caste_code=request.caste_code,
        caste_description=request.caste_description,
        qualification=request.qualification,
        specialization=request.specialization,
        native_place=request.native_place,
        native_dist_code=request.native_dist_code,
        native_district=request.native_district,
        date_of_promotion_to_present_post=request.date_of_promotion_to_present_post,
        date_from_working_in_present_place=request.date_from_working_in_present_place,
        date_of_probation_declared=request.date_of_probation_declared,
        date_of_confirmation=request.date_of_confirmation,
        date_of_splgrade_12yrs=request.date_of_splgrade_12yrs,
        date_of_splgrade_20yrs=request.date_of_splgrade_20yrs,
        opted_zone_while_appointment=request.opted_zone_while_appointment,
        opted_region_while_appointment=request.opted_region_while_appointment,
        opted_division_while_appointment=request.opted_division_while_appointment,
        physically_handicapped_falg=request.physically_handicapped_falg,
        nature_of_appointment=request.nature_of_appointment,
        nature_of_promotion=request.nature_of_promotion
    )

    db.add(e)
    db.commit()
    db.refresh(e)

    return e

def get_current_user(data: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_token(data, credentials_exception)

# reading all the employees detail
@app.get('/', tags=['Employees'])
def read_emps(db: Session = Depends(get_db), current_user:schema.User=Depends(get_current_user)):
    emp= db.query(models.Employee).all()
    return(emp, current_user)


# read a perticular employee detail

@app.get('/{employee_id}', status_code=status.HTTP_200_OK, tags=['Employees'])
def read_emp(employee_id,  db:Session=Depends(get_db)):
    emp= db.query(models.Employee).filter(models.Employee.employee_id==employee_id).first()
    if not emp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Employee with employee_id {employee_id} is not available")
    return emp



# create user
pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.post('/user', tags=['Userlogin'])
def create_user(request:schema.User, db:Session=Depends(get_db)):

    new_user= models.User(Name=request.Name, email=request.email, password=hashing.Hash.bcrypt(request.password))


    # if '@' not in new_user.email:
    #     return {"status":"Error provide valid email"}
    # else:
    #     return {"status":"Successfuly user Created","User":new_user}

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


#  authentication

@app.post("/token", tags=['Authentication'])
async def login_access(request:OAuth2PasswordRequestForm= Depends(),db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.email==request.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incorrect username or password")

    # if not Hash.verify(user.password, request.password):
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="Incorrect  password")

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}



def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



def verify_token(token:str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schema.TokenData(email=email)
    except JWTError:
        raise credentials_exception



@app.put('/', tags=['Employees'])
def update(employee_id, request: schema.Employee, db:Session=Depends(get_db)):
    emp=db.query(models.Employee).filter(models.Employee.employee_id==employee_id)
    if not emp.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"employee not found with employee_id {employee_id}")

    db.commit()
    return emp.update(request)



@app.patch('/u', tags=['Employees'])
def update_emp(request:schema.Employee, db:Session=Depends(get_db)):

    emp = db.query(models.Employee).filter(models.Employee.employee_id == models.Employee.employee_id).first()
    if emp is None:
        return None

    # setattr(emp, 'exclude_unset', True)
    # Update model class variable from requested fields
    for var, value in vars(request).items():
        setattr(emp, var, value) if value else None

        # emp.modified = modified_now
    db.add(emp)
    db.commit()
    db.refresh(emp)
    return emp
    # except Exception as err:
    #     print(str(err))
    #     return str(err)


@app.patch("/emp/{id}", response_model=schema.Employee)
def update_emp(id: str, emp: schema.Employee):
    with Session(engine) as session:
        db_emp = session.get(models.Employee,id)
        if not db_emp:
            raise HTTPException(status_code=404, detail="employee not found")
        emp_data = emp.dict(exclude_unset=True)
        for key, value in emp_data.items():
            setattr(db_emp, key, value)
        session.add(db_emp)
        session.commit()
        session.refresh(db_emp)
        return db_emp


# @app.put("/e")
# def up(request:Request):
#     employee_id = request.get('employee_id')
#     employee_update_info = request
#     print(employee_update_info, employee_id)


# @app.patch("/items/{employee_id}", response_model=schema.Employee)
# async def update_item(request:schema.Employee,db:Session(get_db)):
#     emp= Session.query(models.Employee).get('employee_id')
#     stored_item_data = models.Employee.filter(models.Employee.employee_id)
#     stored_item_model = schema.Employee(**stored_item_data)
#     update_data = models.Employee.dict(exclude_unset=True)
#     updated_item = stored_item_model.copy(update=update_data)
#     models.Employee.employee_id = jsonable_encoder(updated_item, request,emp)
#     return updated_item



@app.post("/login/", tags=['loginform'])
async def login(username: str = Form(), password: str = Form()):
    return {"username": username, "password":password}




# @app.post("/files/")
# async def create_file(file: bytes = File()):
#     return {"file_size": len(file)}


@app.post("/", tags=['file'])
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}


@app.post("/upload files")
async def create_file(
    file: bytes = File(), fileb: UploadFile = File(), token: str = Form()
):
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type,
    }


from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
