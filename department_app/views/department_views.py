from flask import render_template, redirect, url_for, request
from . import web_app
from department_app.rest import DepartmentListAPI, DepartmentAPI
from department_app.service import DepartmentService


@web_app.route('/department/', endpoint="departments", methods=['GET', 'POST'])
def departments():
    deps = DepartmentListAPI.get()
    deps = list(map(lambda dep: DepartmentAPI.get(dep_id=dep.get("id")), deps))

    return render_template("departments.html", departments=deps)


@web_app.route('/department/add', endpoint="department_add", methods=['GET', 'POST'])
def department_add(department_base=None, errors=None):
    if request.method == 'POST':
        response = DepartmentListAPI.post()
        if 200 <= response[1] < 300:
            return redirect(url_for("web_app.departments"))
        errors = [response[0].get("message")]
        department_base = request.form

    return render_template("department_add.html", department_base=department_base, errors=errors)


@web_app.route('/department/<string:dep_id>/edit', endpoint="department_edit", methods=['GET', 'POST'])
def department_edit(dep_id, errors=None):
    if request.method == 'POST':
        response = DepartmentAPI.put(dep_id=dep_id)
        if 200 <= response[1] < 300:
            return redirect(url_for("web_app.departments"))
        else:
            errors = [response[0].get("message")]

    department = DepartmentAPI.get(dep_id=dep_id)
    return render_template("department_edit.html", department=department, errors=errors)


@web_app.route('/department/<string:dep_id>/delete', endpoint="department_delete", methods=['GET'])
def department_delete(dep_id):
    DepartmentAPI.delete(dep_id=dep_id)
    return redirect(url_for("web_app.departments"))
