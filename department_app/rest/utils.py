from typing import Union


def format_exception_message(exception: Union[Exception, str]):
    if isinstance(exception, str):
        return {'message': exception}
    return format_exception_message(str(exception))
