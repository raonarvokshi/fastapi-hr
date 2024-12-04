from fastapi import FastAPI, HTTPException
from models import Employee, EmployeeBase, CreateEmployee
from database import create_connection, create_table
from typing import List

app = FastAPI(
    title="Employee Managment API",
    description="Employee Managment web application",
    version="1.0.0"
)

create_table()


@app.get("/")
def root():
    return {"Message": "Hello Everyone welcome to the best employee managment web app go to /docs for more"}


@app.post("/add/employee", response_model=Employee)
def add_employee(employee: CreateEmployee):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        "Insert into employees (full_name, email, gender, job_title, salary) Values (?, ?, ?, ?, ?)", (employee.full_name, employee.email, employee.gender, employee.job_title, employee.salary))
    conn.commit()
    employee_id = cursor.lastrowid
    conn.close()
    return Employee(id=employee_id, full_name=employee.full_name, email=employee.full_name, gender=employee.gender, job_title=employee.job_title, salary=employee.salary)


@app.get("/employees", response_model=List[Employee])
def get_employees():
    conn = create_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM employees"
    cursor.execute(query)
    employees = cursor.fetchall()
    conn.close()
    return [
        Employee(id=employee[0], full_name=employee[1], email=employee[2],
                 gender=employee[3], job_title=employee[4], salary=employee[5])
        for employee in employees
    ]


# @app.get("/employee/{employee_id}", response_model=AddEmployee)
# def get_employee_by_id(employe_id: int):
#     conn = create_connection()
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM employees WHERE id=?", (employe_id, ))
#     employee = cursor.fetchone()
#     conn.close()

#     if not employee:
#         raise HTTPException(status_code=404,
#                             detail=f"Employee with id {employe_id} not found")

#     return AddEmployee(
#         full_name=employee[1],
#         email=employee[2],
#         gender=employee[3],
#         job_title=employee[4],
#         salary=employee[5]
#     )


@app.put("/update/employee/{employee_id}", response_model=Employee)
def update_employee(employee_id: int, employee: CreateEmployee):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE employees SET full_name=?, email=?, gender=?, job_title=?, salary=? WHERE id=?",
        (employee.full_name, employee.email, employee.gender,
         employee.job_title, employee.salary, employee_id)
    )

    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(
            status_code=404,
            detail=f"Employee with the id {employee_id} not found"
        )

    conn.commit()
    conn.close()
    return Employee(
        id=employee_id,
        full_name=employee.full_name,
        email=employee.email,
        gender=employee.gender,
        job_title=employee.job_title,
        salary=employee.salary
    )


@app.delete("/delete/employee/{employee_id}", response_model=dict)
def delete_employee(employee_id: int):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM employees where id=?", (employee_id,))
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Employee not found")
    conn.commit()
    conn.close()
    return {"Details": "Employee deleted successfully!"}
