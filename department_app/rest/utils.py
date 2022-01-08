"""
Module with utility functions to work with Rest API.
"""

from typing import Union


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

def employee_dict_from_http_dict(http_dict):
    ...