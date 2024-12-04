from pydantic import BaseModel


class EmployeeBase(BaseModel):
    full_name: str
    email: str
    gender: str
    job_title: str
    salary: float


class CreateEmployee(EmployeeBase):
    pass


class Employee(EmployeeBase):
    id: int
