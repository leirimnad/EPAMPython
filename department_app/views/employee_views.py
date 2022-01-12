"""
Module which contains web views for employee-related parts of the app.
"""
from flask import render_template, redirect, url_for, request
from department_app.rest import EmployeeListAPI, EmployeeAPI, DepartmentAPI, DepartmentListAPI
from .web_app import web_app


@web_app.route('/employee/', endpoint="employees", methods=['GET'])
def employees():
    """
    View for displaying a full or filtered list of the employees.
    @return: rendered template with the list of the employees
    """
    emps = EmployeeListAPI.get()
    department_set = set()
    for emp in emps:
        emp["department"] = DepartmentAPI.get(emp.get("department_id"))
        department_set.add(emp.get("department_id"))

    return render_template("employees.html", employees=emps, department_count=len(department_set))


@web_app.route('/employee/add', endpoint="employee_add", methods=['GET', 'POST'])
def employee_add(employee_base=None, errors=None):
    """
    View for displaying a form for adding the employee.
    @param employee_base: employee as a dictionary to fill the form with
    @param errors: list of string representations of errors to display on the page
    @return: rendered template with a form for adding the employee
    """
    if request.method == 'POST':
        response = EmployeeListAPI.post()
        if 200 <= response[1] < 300:
            return redirect(url_for("web_app.employees"))
        errors = [response[0].get("message")]
        employee_base = request.form

    deps = DepartmentListAPI.get()

    return render_template("employee_add.html",
                           employee_base=employee_base, available_departments=deps, errors=errors)


@web_app.route('/employee/<string:emp_id>/edit', endpoint="employee_edit", methods=['GET', 'POST'])
def employee_edit(emp_id, errors=None):
    """
    View for displaying a form for editing the employee.
    @param emp_id: employee id to edit
    @param errors: list of string representations of errors to display on the page
    @return: rendered template with a form for editing the employee
    """
    if request.method == 'POST':
        response = EmployeeAPI.put(emp_id=emp_id)
        if 200 <= response[1] < 300:
            return redirect(url_for("web_app.employees"))
        errors = [response[0].get("message")]

    deps = DepartmentListAPI.get()
    employee = EmployeeAPI.get(emp_id=emp_id)
    return render_template("employee_edit.html",
                           employee=employee, available_departments=deps, errors=errors)


@web_app.route('/employee/<string:emp_id>/delete', endpoint="employee_delete", methods=['GET'])
def employee_delete(emp_id):
    """
    View to be called for deleting the employee.
    @param emp_id: employee id to delete
    @return: redirect response for redirecting to the list of employee
    """
    EmployeeAPI.delete(emp_id=emp_id)
    return redirect(url_for("web_app.employees"))
