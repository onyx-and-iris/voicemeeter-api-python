class InstallError(Exception):
    """Exception raised when installation errors occur"""


class CAPIError(Exception):
    """Exception raised when the C-API returns error values"""


class VMError(Exception):
    """Exception raised when general errors occur"""
