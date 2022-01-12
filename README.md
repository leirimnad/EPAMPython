### EPAM Python Project

[![Coverage Status](https://coveralls.io/repos/github/leirimnad/EPAMPython/badge.svg?branch=main)](https://coveralls.io/github/leirimnad/EPAMPython?branch=main)
[![Build Status](https://app.travis-ci.com/leirimnad/EPAMPython.svg?branch=main)](https://app.travis-ci.com/leirimnad/EPAMPython)

# Department managing app

### A simple web application for managing departments and employees. 

## Description

**The web application can:**
- display a list of departments
- display the average salary (calculated automatically) for each department
- display a list of employees in the departments
- display the salary for each employee
- search for employees born on a certain date or in the period between dates
- change (add / edit / delete) the above data

> Software requirements are stated in the [SRS.md](documentation/SRS.md) file


## Running the app

### Installing requirements

Before running the application, you may install the project requirements using `pip`:
```bash
pip install -r requirements.txt
```

### Database configuration

For the application to run, the MySQL database should be set up.

Database credentials are read by the application from the environmental variables.

**Before starting an app (manually or using Gunicorn), please set the next environmental variables:**

- `MYSQL_DB_USER`: MySQL user

- `MYSQL_DB_PASSWORD`: MySQL password

- `MYSQL_DB_HOST`: MySQL host (and port, separated by `:`)

- `MYSQL_DB_DATABASE`: MySQL database name

> The simplest way to specify environmental variables is to insert the following before the bash commands:
>
> ```bash
> MYSQL_DB_USER="Boss" MYSQL_DB_PASSWORD="MyPassword" MYSQL_DB_HOST="localhost" MYSQL_DB_DATABASE="my_database"
> ```

### Populating the database

To populate the database with the small amount of test data, run `populate.py` from `help` module.

```bash
python -m department_app.help.populate
```

> Don't forget about the environmental variables!

### Starting the app without using the WSGI

If you don't want to use WSGI, you can start an app by running:

```bash
python -m department_app.app
```

> Don't forget about the environmental variables!


### Starting the app using the WSGI

If you want to start an app using Gunicorn, try the following:

```bash
gunicorn department_app.app:app
```

Specify the amount of workers and the host as parameters:

```-w 4 ``` for using 4 workers

```--b 127.0.0.1:7772``` for starting an app on *127.0.0.1:7772*


> Still, don't forget about the environmental variables!

## Using app's API

App supports REST. You can access the following URLs:
- `/api/department/` for managing departments
- `/api/employee/` for managing employees

### Managing departments

- Send a **GET** request to `/api/department/`
_to **GET** the list of all the departments_

- Send a **POST** request to `/api/department/`
_to **CREATE** a department_. 
  - Specify the next data:
    - `name` - the name of the department
    - `description` - the department's description
  - The created department will be returned to you if one has been created successfully.

- Send a **POST** request to `/api/department/<dep_id>`
_to **FULLY UPDATE** the department with id `<dep_id>`_. 
  - Specify the next data:
    - `name` - the new name of the department
    - `description` - the department's new description
  - If any of the fields is not specified, an error will be returned
  - The updated department will be returned to you if one has been updated successfully.


- Send a **PATCH** request to `/api/department/<dep_id>`
_to **UPDATE SOME FIELDS** of the department with id `<dep_id>`_. 
  - Specify the next data:
    - `name` *(optional)* - the new name of the department
    - `description` *(optional)* - the department's new description
  - If any of the fields is not specified, the corresponding field of the department will not be updated
  - The updated department will be returned to you if one has been updated successfully.

- Send a **DELETE** request to `/api/department/<dep_id>`
_to **DELETE** the department with id `<dep_id>`_. 

### Managing employees

- Send a **GET** request to `/api/employee/`
_to **GET** the list of all the employees_

- Send a **POST** request to `/api/employee/`
_to **CREATE** an employee_. 
  - Specify the next data:
    - `name` - the name of the employee
    - `department_id` - the id of the department of the employee
    - `job` - the job of the employee
    - `birth_date` - the birth_date of the employee in `dd/mm/yyyy` format
    - `salary` - the salary of the employee
  - The created employee will be returned to you if one has been created successfully.

- Send a **POST** request to `/api/employee/<emp_id>`
_to **FULLY UPDATE** the employee with id `<emp_id>`_. 
  - Specify the next data:
    - `name` - the name of the employee
    - `department_id` - the id of the department of the employee
    - `job` - the job of the employee
    - `birth_date` - the birth_date of the employee in `dd/mm/yyyy` format
    - `salary` - the salary of the employee
  - If any of the fields is not specified, an error will be returned
  - The updated employee will be returned to you if one has been updated successfully.


- Send a **PATCH** request to `/api/employee/<emp_id>`
_to **UPDATE SOME FIELDS** of the employee with id `<emp_id>`_. 
  - Specify the next data:
    - `name` *(optional)* - the name of the employee
    - `department_id` *(optional)* - the id of the department of the employee
    - `job` *(optional)* - the job of the employee
    - `birth_date` *(optional)* - the birth_date of the employee in `dd/mm/yyyy` format
    - `salary` *(optional)* - the salary of the employee
  - If any of the fields is not specified, the corresponding field of the department will not be updated
  - The updated employee will be returned to you if one has been updated successfully.

- Send a **DELETE** request to `/api/employee/<emp_id>`
_to **DELETE** the employee with id `<emp_id>`_. 