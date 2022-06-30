from typing import Optional

from pydantic import BaseModel

class Employee(BaseModel):

    # Name :str
    # contact :str
    # email :str
    # department :str
    # salary:str

    unit_code:str
    category_code: str
    employee_id: str
    name: str
    gender: str
    relegion: str
    relegion_description: str
    nationality: str
    factory_act_flag: str
    designation_code: str
    class_of_employee: str
    weekly_off_day: str
    direct_recruity_promotee: str
    section_code: str
    dob: str
    initial_appointment_date: str
    date_of_regular: str
    date_of_last_increment_drawn: str
    date_of_medical_examination_done: str
    basic_pay: str
    protected_pay: str
    grade_pay: str
    special_pay: str
    family_planning_pay: str
    telangana_incentive: str
    graduation_increment: str
    equalisation_allowance: str
    special_allowance: str
    special_allowance1: str
    father_spouse_name: str
    caste_code: str
    caste_description: str
    subcast_code :str
    subcast_description: str
    qualification: str
    specialization: str
    native_place: str
    native_dist_code: str
    native_district: str
    date_of_promotion_to_present_post: str
    date_from_working_in_present_place: str
    date_of_probation_declared: str
    date_of_confirmation: str
    date_of_splgrade_12yrs: str
    date_of_splgrade_20yrs: str
    opted_zone_while_appointment: str
    opted_region_while_appointment: str
    opted_division_while_appointment: str
    physically_handicapped_falg: str
    nature_of_appointment: str
    nature_of_promotion: str


    class Config:
        orm_mode = True


class User(BaseModel):
    Name: str
    email:str
    password:str


class Login(BaseModel):
    username: str
    password:str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[ str] = None


