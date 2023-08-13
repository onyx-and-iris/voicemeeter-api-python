class VMError(Exception):
    """Base VM Exception class. Raised when general errors occur."""


class InstallError(VMError):
    """Exception raised when installation errors occur"""


class CAPIError(VMError):
    """Exception raised when the C-API returns an error code"""

    def __init__(self, fn_name, code):
        self.fn_name = fn_name
        self.code = code
        if self.code == -9:
            message = " ".join(
                (
                    f"no bind for {self.fn_name}.",
                    "are you using an old version of the API?",
                )
            )
        else:
            message = f"{self.fn_name} returned {self.code}"
        super().__init__(message)
