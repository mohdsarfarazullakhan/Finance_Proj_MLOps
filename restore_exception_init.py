from pathlib import Path

path = Path(__file__).resolve().parent / "src" / "exception" / "__init__.py"
path.write_text(
    "import sys\n"
    "import logging\n\n"
    "def error_message_detail(error: Exception, error_detail: sys) -> str:\n"
    "    \"\"\"Extracts detailed error information including file name, line number, and the error message.\n\n"
    "    :param error: The exception that occurred.\n"
    "    :param error_detail: The sys module to access traceback details.\n"
    "    :return: A formatted error message string.\n"
    "    \"\"\"\n"
    "    _, _, exc_tb = error_detail.exc_info()\n"
    "    file_name = exc_tb.tb_frame.f_code.co_filename\n"
    "    line_number = exc_tb.tb_lineno\n"
    "    error_message = f\"Error occurred in python script: [{file_name}] at line number [{line_number}]: {str(error)}\"\n"
    "    logging.error(error_message)\n"
    "    return error_message\n\n"
    "class MyException(Exception):\n"
    "    \"\"\"Custom exception class for handling errors.\n"
    "    \"\"\"\n"
    "    def __init__(self, error_message: str, error_detail: sys):\n"
    "        super().__init__(error_message)\n"
    "        self.error_message = error_message_detail(error_message, error_detail)\n\n"
    "    def __str__(self) -> str:\n"
    "        return self.error_message\n"
)
print(f'Wrote {path}')
