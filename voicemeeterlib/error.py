class InstallError(Exception):
    """errors related to installation"""

    pass


class CAPIError(Exception):
    """errors related to low-level C API calls"""

    pass


class VMError(Exception):
    """general errors"""

    pass
