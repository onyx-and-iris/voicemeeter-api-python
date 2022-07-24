import ctypes as ct
from abc import ABCMeta
from ctypes.wintypes import CHAR, FLOAT, LONG, WCHAR

from .error import CAPIError
from .inst import libc


class CBindings(metaclass=ABCMeta):
    """
    C bindings defined here.

    Maps expected ctype argument and res types for each binding.
    """

    vm_login = libc.VBVMR_Login
    vm_login.restype = LONG
    vm_login.argtypes = None

    vm_logout = libc.VBVMR_Logout
    vm_logout.restype = LONG
    vm_logout.argtypes = None

    vm_runvm = libc.VBVMR_RunVoicemeeter
    vm_runvm.restype = LONG
    vm_runvm.argtypes = [LONG]

    vm_get_type = libc.VBVMR_GetVoicemeeterType
    vm_get_type.restype = LONG
    vm_get_type.argtypes = [ct.POINTER(LONG)]

    vm_get_version = libc.VBVMR_GetVoicemeeterVersion
    vm_get_version.restype = LONG
    vm_get_version.argtypes = [ct.POINTER(LONG)]

    vm_mdirty = libc.VBVMR_MacroButton_IsDirty
    vm_mdirty.restype = LONG
    vm_mdirty.argtypes = None

    vm_get_buttonstatus = libc.VBVMR_MacroButton_GetStatus
    vm_get_buttonstatus.restype = LONG
    vm_get_buttonstatus.argtypes = [LONG, ct.POINTER(FLOAT), LONG]

    vm_set_buttonstatus = libc.VBVMR_MacroButton_SetStatus
    vm_set_buttonstatus.restype = LONG
    vm_set_buttonstatus.argtypes = [LONG, FLOAT, LONG]

    vm_pdirty = libc.VBVMR_IsParametersDirty
    vm_pdirty.restype = LONG
    vm_pdirty.argtypes = None

    vm_get_parameter_float = libc.VBVMR_GetParameterFloat
    vm_get_parameter_float.restype = LONG
    vm_get_parameter_float.argtypes = [ct.POINTER(CHAR), ct.POINTER(FLOAT)]

    vm_set_parameter_float = libc.VBVMR_SetParameterFloat
    vm_set_parameter_float.restype = LONG
    vm_set_parameter_float.argtypes = [ct.POINTER(CHAR), FLOAT]

    vm_get_parameter_string = libc.VBVMR_GetParameterStringW
    vm_get_parameter_string.restype = LONG
    vm_get_parameter_string.argtypes = [ct.POINTER(CHAR), ct.POINTER(WCHAR * 512)]

    vm_set_parameter_string = libc.VBVMR_SetParameterStringW
    vm_set_parameter_string.restype = LONG
    vm_set_parameter_string.argtypes = [ct.POINTER(CHAR), ct.POINTER(WCHAR)]

    vm_set_parameter_multi = libc.VBVMR_SetParameters
    vm_set_parameter_multi.restype = LONG
    vm_set_parameter_multi.argtypes = [ct.POINTER(CHAR)]

    vm_get_level = libc.VBVMR_GetLevel
    vm_get_level.restype = LONG
    vm_get_level.argtypes = [LONG, LONG, ct.POINTER(FLOAT)]

    vm_get_num_indevices = libc.VBVMR_Input_GetDeviceNumber
    vm_get_num_indevices.restype = LONG
    vm_get_num_indevices.argtypes = None

    vm_get_desc_indevices = libc.VBVMR_Input_GetDeviceDescW
    vm_get_desc_indevices.restype = LONG
    vm_get_desc_indevices.argtypes = [
        LONG,
        ct.POINTER(LONG),
        ct.POINTER(WCHAR * 256),
        ct.POINTER(WCHAR * 256),
    ]

    vm_get_num_outdevices = libc.VBVMR_Output_GetDeviceNumber
    vm_get_num_outdevices.restype = LONG
    vm_get_num_outdevices.argtypes = None

    vm_get_desc_outdevices = libc.VBVMR_Output_GetDeviceDescW
    vm_get_desc_outdevices.restype = LONG
    vm_get_desc_outdevices.argtypes = [
        LONG,
        ct.POINTER(LONG),
        ct.POINTER(WCHAR * 256),
        ct.POINTER(WCHAR * 256),
    ]

    vm_get_midi_message = libc.VBVMR_GetMidiMessage
    vm_get_midi_message.restype = LONG
    vm_get_midi_message.argtypes = [ct.POINTER(CHAR * 1024), LONG]

    def call(self, func):
        res = func()
        if res != 0:
            raise CAPIError(f"Function {func.func.__name__} returned {res}")
