"""
Module with utility functions to work with Rest API.
"""
import datetime
import logging
import re
from typing import Union, Optional

from flask import request

from department_app.service import DepartmentService


def format_exception_message(exception: Union[Exception, str] = None):
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
        birth_date_str = http_dict.get("birth_date")
        res["birth_date"] = parse_date(birth_date_str)
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


def log_unhandled_exception(exc: Exception):
    """
    Logs a warning about an unexpected and unhandled exception.
    @param exc: Exception to log
    """
    logging.warning("An exception has happened while handling %s "
                    "request to %s:", request.method, request.url,
                    exc_info=exc)


def parse_date(date_string: str, required: bool = True) -> Optional[datetime.date]:
    """
    Parses a date of YYYY-MM-DD or DD/MM/YY format into a date instance.
    @param date_string: string containing a date
    @param required: if True, date_string will be required to not be None or empty,
    otherwise None and empty strings will return None
    @return: date instance or None if date_string is None and required is False
    """
    try:
        if not date_string and not required:
            return None
        if re.match(r"\d\d\d\d-\d\d-\d\d", date_string):
            return datetime.datetime.strptime(date_string, "%Y-%m-%d").date()
        if re.match(r"\d\d/\d\d/\d\d\d\d", date_string):
            return datetime.datetime.strptime(date_string, "%d/%m/%Y").date()
        raise ValueError("Provide the date in %Y-%m-%d or %d/%m/%Y format!")
    except (TypeError, ValueError) as ex:
        raise ValueError("Date must be in %d/%m/%Y format") from ex
