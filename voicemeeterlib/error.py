class VMError(Exception):
    """Base VM Exception class. Raised when general errors occur."""

    def __init__(self, msg):
        self.message = msg
        super().__init__(self.message)

    def __str__(self):
        return f"{type(self).__name__}: {self.message}"


class InstallError(VMError):
    """Exception raised when installation errors occur"""


class CAPIError(VMError):
    """Exception raised when the C-API returns an error code"""

    def __init__(self, fn_name, code, msg=None):
        self.fn_name = fn_name
        self.code = code
        super(CAPIError, self).__init__(msg if msg else f"{fn_name} returned {code}")
