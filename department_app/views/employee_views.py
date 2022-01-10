from flask import render_template, redirect, url_for, request
from . import web_app
from department_app.rest import EmployeeListAPI, EmployeeAPI, DepartmentAPI, DepartmentListAPI


@web_app.route('/employee/', endpoint="employees", methods=['GET'])
def employees(filter_department=None, filter_date_start=None, filter_date_end=None):
    emps = EmployeeListAPI.get()
    department_set = set()
    for emp in emps:
        emp["department"] = DepartmentAPI.get(emp.get("department_id"))
        department_set.add(emp.get("department_id"))

    return render_template("employees.html", employees=emps, department_count=len(department_set))


@web_app.route('/employee/add', endpoint="employee_add", methods=['GET', 'POST'])
def employee_add(employee_base=None, errors=None):
    if request.method == 'POST':
        response = EmployeeListAPI.post()
        if 200 <= response[1] < 300:
            return redirect(url_for("web_app.employees"))
        errors = [response[0].get("message")]
        employee_base = request.form

    deps = DepartmentListAPI.get()

    return render_template("employee_add.html", employee_base=employee_base, available_departments=deps, errors=errors)


@web_app.route('/employee/<string:emp_id>/edit', endpoint="employee_edit", methods=['GET', 'POST'])
def employee_edit(emp_id, errors=None):
    if request.method == 'POST':
        response = EmployeeAPI.put(emp_id=emp_id)
        if 200 <= response[1] < 300:
            return redirect(url_for("web_app.employees"))
        else:
            errors = [response[0].get("message")]

    deps = DepartmentListAPI.get()
    employee = EmployeeAPI.get(emp_id=emp_id)
    return render_template("employee_edit.html", employee=employee, available_departments=deps, errors=errors)


@web_app.route('/employee/<string:emp_id>/delete', endpoint="employee_delete", methods=['GET'])
def employee_delete(emp_id):
    EmployeeAPI.delete(emp_id=emp_id)
    return redirect(url_for("web_app.employees"))
