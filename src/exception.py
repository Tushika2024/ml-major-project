import sys
from src.logger import logging

def error_message_detail(error_message,error_detail:sys)-> str:
    _,_,exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno
    detailed_message = f"Error occurred in file: {file_name} at line: {line_number} with message: {error_message}"
    return detailed_message

class CustomException(Exception):
    """A custom exception class that extends the built-in Exception class."""
    def __init__(self,error_message,error_detail:sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message,error_detail=error_detail)

    def __str__(self):
        return f"CustomException: {self.error_message}"

# if __name__ == "__main__":
#     try:
#         a = 1 / 0
#     except Exception as e:
#         logging.info("An exception occurred.")
#         ce=CustomException(e,sys)
#         logging.info(ce)
#         print(ce)