"""
Module with utility functions to work with Rest API.
"""
import datetime
from typing import Union
from department_app.service import DepartmentService


def format_exception_message(exception: Union[Exception, str]):
    """
    Formats Exception into an appropriate form for sending through HTTP.
    @param exception: Exception instance or exception description as string
    @return: formatted exception
    """
    if exception is None:
        return format_exception_message("An error has happened.")
    if isinstance(exception, str):
        return {'message': exception}
    return format_exception_message(str(exception))


# pylint: disable=too-many-branches
def employee_dict_from_http_dict(http_dict: dict, required=True, exclude_keys: list = None) -> dict:
    """
    Transforms http form dictionary into a dictionary with cleaned data.
    @param http_dict: form dictionary
    @param required: if set as True, an exception will be raised if field is not stated
    @param exclude_keys: keys to exclude from the result dictionary
    @return: dictionary with the cleaned data
    """
    res = {}

    if required and "name" not in http_dict.keys():
        raise ValueError("Name is not provided")
    res["name"] = http_dict.get("name")

    if "department_id" in http_dict.keys():
        res["department"] = DepartmentService.get_department_by_id(http_dict.get("department_id"))
    elif required:
        raise ValueError("Department is not provided")

    if required and "job" not in http_dict.keys():
        raise ValueError("Job is not provided")
    res["job"] = http_dict.get("job")

    if "birth_date" in http_dict.keys():
        try:
            birth_date_str = http_dict.get("birth_date")
            res["birth_date"] = datetime.datetime.strptime(birth_date_str, "%d/%m/%Y").date()
        except (TypeError, ValueError) as ex:
            raise ValueError("Date must be in %d/%m/%Y format") from ex
    elif required:
        raise ValueError("Birthdate is not provided")

    if "salary" in http_dict.keys():
        if not http_dict.get('salary').isnumeric():
            raise ValueError("Salary must be numeric")
        res["salary"] = int(http_dict.get("salary"))
    elif required:
        raise ValueError("Salary is not provided")

    if exclude_keys:
        for key in res:
            if key in exclude_keys:
                res.pop(key)

    return res
