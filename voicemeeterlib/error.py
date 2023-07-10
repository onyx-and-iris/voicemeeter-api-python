class InstallError(Exception):
    """Exception raised when installation errors occur"""


class CAPIError(Exception):
    """Exception raised when the C-API returns error values"""

    def __init__(self, fn_name, code, msg=None):
        self.fn_name = fn_name
        self.code = code
        self.message = msg if msg else f"{fn_name} returned {code}"
        super().__init__(self.message)

    def __str__(self):
        return f"{type(self).__name__}: {self.message}"


class VMError(Exception):
    """Exception raised when general errors occur"""
