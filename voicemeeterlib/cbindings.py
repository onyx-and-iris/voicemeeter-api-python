import ctypes as ct
import logging
from ctypes.wintypes import CHAR, FLOAT, LONG, WCHAR

from .error import CAPIError
from .inst import libc

logger = logging.getLogger(__name__)


class CBindings:
    """Class responsible for defining C function bindings.

    Wrapper methods are provided for each C function to handle error checking and logging.
    """

    logger_cbindings = logger.getChild('CBindings')

    bind_login = libc.VBVMR_Login
    bind_login.restype = LONG
    bind_login.argtypes = None

    bind_logout = libc.VBVMR_Logout
    bind_logout.restype = LONG
    bind_logout.argtypes = None

    bind_run_voicemeeter = libc.VBVMR_RunVoicemeeter
    bind_run_voicemeeter.restype = LONG
    bind_run_voicemeeter.argtypes = [LONG]

    bind_get_voicemeeter_type = libc.VBVMR_GetVoicemeeterType
    bind_get_voicemeeter_type.restype = LONG
    bind_get_voicemeeter_type.argtypes = [ct.POINTER(LONG)]

    bind_get_voicemeeter_version = libc.VBVMR_GetVoicemeeterVersion
    bind_get_voicemeeter_version.restype = LONG
    bind_get_voicemeeter_version.argtypes = [ct.POINTER(LONG)]

    if hasattr(libc, 'VBVMR_MacroButton_IsDirty'):
        bind_macro_button_is_dirty = libc.VBVMR_MacroButton_IsDirty
        bind_macro_button_is_dirty.restype = LONG
        bind_macro_button_is_dirty.argtypes = None

    if hasattr(libc, 'VBVMR_MacroButton_GetStatus'):
        bind_macro_button_get_status = libc.VBVMR_MacroButton_GetStatus
        bind_macro_button_get_status.restype = LONG
        bind_macro_button_get_status.argtypes = [LONG, ct.POINTER(FLOAT), LONG]

    if hasattr(libc, 'VBVMR_MacroButton_SetStatus'):
        bind_macro_button_set_status = libc.VBVMR_MacroButton_SetStatus
        bind_macro_button_set_status.restype = LONG
        bind_macro_button_set_status.argtypes = [LONG, FLOAT, LONG]

    bind_is_parameters_dirty = libc.VBVMR_IsParametersDirty
    bind_is_parameters_dirty.restype = LONG
    bind_is_parameters_dirty.argtypes = None

    bind_get_parameter_float = libc.VBVMR_GetParameterFloat
    bind_get_parameter_float.restype = LONG
    bind_get_parameter_float.argtypes = [ct.POINTER(CHAR), ct.POINTER(FLOAT)]

    bind_set_parameter_float = libc.VBVMR_SetParameterFloat
    bind_set_parameter_float.restype = LONG
    bind_set_parameter_float.argtypes = [ct.POINTER(CHAR), FLOAT]

    bind_get_parameter_string_w = libc.VBVMR_GetParameterStringW
    bind_get_parameter_string_w.restype = LONG
    bind_get_parameter_string_w.argtypes = [ct.POINTER(CHAR), ct.POINTER(WCHAR * 512)]

    bind_set_parameter_string_w = libc.VBVMR_SetParameterStringW
    bind_set_parameter_string_w.restype = LONG
    bind_set_parameter_string_w.argtypes = [ct.POINTER(CHAR), ct.POINTER(WCHAR)]

    bind_set_parameters = libc.VBVMR_SetParameters
    bind_set_parameters.restype = LONG
    bind_set_parameters.argtypes = [ct.POINTER(CHAR)]

    bind_get_level = libc.VBVMR_GetLevel
    bind_get_level.restype = LONG
    bind_get_level.argtypes = [LONG, LONG, ct.POINTER(FLOAT)]

    bind_input_get_device_number = libc.VBVMR_Input_GetDeviceNumber
    bind_input_get_device_number.restype = LONG
    bind_input_get_device_number.argtypes = None

    bind_input_get_device_desc_w = libc.VBVMR_Input_GetDeviceDescW
    bind_input_get_device_desc_w.restype = LONG
    bind_input_get_device_desc_w.argtypes = [
        LONG,
        ct.POINTER(LONG),
        ct.POINTER(WCHAR * 256),
        ct.POINTER(WCHAR * 256),
    ]

    bind_output_get_device_number = libc.VBVMR_Output_GetDeviceNumber
    bind_output_get_device_number.restype = LONG
    bind_output_get_device_number.argtypes = None

    bind_output_get_device_desc_w = libc.VBVMR_Output_GetDeviceDescW
    bind_output_get_device_desc_w.restype = LONG
    bind_output_get_device_desc_w.argtypes = [
        LONG,
        ct.POINTER(LONG),
        ct.POINTER(WCHAR * 256),
        ct.POINTER(WCHAR * 256),
    ]

    bind_get_midi_message = libc.VBVMR_GetMidiMessage
    bind_get_midi_message.restype = LONG
    bind_get_midi_message.argtypes = [ct.POINTER(CHAR * 1024), LONG]

    def _call(self, func, *args, ok=(0,), ok_exp=None):
        """Call a C function and handle errors."""
        try:
            res = func(*args)
            if ok_exp is None:
                if res not in ok:
                    raise CAPIError(func.__name__, res)
            elif not ok_exp(res) and res not in ok:
                raise CAPIError(func.__name__, res)
            return res
        except CAPIError as e:
            self.logger_cbindings.exception(f'{type(e).__name__}: {e}')
            raise

    def login(self, **kwargs):
        """Login to Voicemeeter API"""
        return self._call(self.bind_login, **kwargs)

    def logout(self):
        """Logout from Voicemeeter API"""
        return self._call(self.bind_logout)

    def run_voicemeeter(self, value):
        """Run Voicemeeter with specified type"""
        return self._call(self.bind_run_voicemeeter, value)

    def get_voicemeeter_type(self, type_ref):
        """Get Voicemeeter type"""
        return self._call(self.bind_get_voicemeeter_type, type_ref)

    def get_voicemeeter_version(self, version_ref):
        """Get Voicemeeter version"""
        return self._call(self.bind_get_voicemeeter_version, version_ref)

    def is_parameters_dirty(self, **kwargs):
        """Check if parameters are dirty"""
        return self._call(self.bind_is_parameters_dirty, **kwargs)

    def macro_button_is_dirty(self, **kwargs):
        """Check if macro button parameters are dirty"""
        if hasattr(self, 'bind_macro_button_is_dirty'):
            return self._call(self.bind_macro_button_is_dirty, **kwargs)
        raise AttributeError('macro_button_is_dirty not available')

    def get_parameter_float(self, param_name, value_ref):
        """Get float parameter value"""
        return self._call(self.bind_get_parameter_float, param_name, value_ref)

    def set_parameter_float(self, param_name, value):
        """Set float parameter value"""
        return self._call(self.bind_set_parameter_float, param_name, value)

    def get_parameter_string_w(self, param_name, buffer_ref):
        """Get string parameter value (Unicode)"""
        return self._call(self.bind_get_parameter_string_w, param_name, buffer_ref)

    def set_parameter_string_w(self, param_name, value):
        """Set string parameter value (Unicode)"""
        return self._call(self.bind_set_parameter_string_w, param_name, value)

    def macro_button_get_status(self, id_, state_ref, mode):
        """Get macro button status"""
        if hasattr(self, 'bind_macro_button_get_status'):
            return self._call(self.bind_macro_button_get_status, id_, state_ref, mode)
        raise AttributeError('macro_button_get_status not available')

    def macro_button_set_status(self, id_, state, mode):
        """Set macro button status"""
        if hasattr(self, 'bind_macro_button_set_status'):
            return self._call(self.bind_macro_button_set_status, id_, state, mode)
        raise AttributeError('macro_button_set_status not available')

    def get_level(self, type_, index, value_ref):
        """Get audio level"""
        return self._call(self.bind_get_level, type_, index, value_ref)

    def input_get_device_number(self, **kwargs):
        """Get number of input devices"""
        return self._call(self.bind_input_get_device_number, **kwargs)

    def output_get_device_number(self, **kwargs):
        """Get number of output devices"""
        return self._call(self.bind_output_get_device_number, **kwargs)

    def input_get_device_desc_w(self, index, type_ref, name_ref, hwid_ref):
        """Get input device description"""
        return self._call(
            self.bind_input_get_device_desc_w, index, type_ref, name_ref, hwid_ref
        )

    def output_get_device_desc_w(self, index, type_ref, name_ref, hwid_ref):
        """Get output device description"""
        return self._call(
            self.bind_output_get_device_desc_w, index, type_ref, name_ref, hwid_ref
        )

    def get_midi_message(self, buffer_ref, length, **kwargs):
        """Get MIDI message"""
        return self._call(self.bind_get_midi_message, buffer_ref, length, **kwargs)

    def set_parameters(self, script):
        """Set multiple parameters via script"""
        return self._call(self.bind_set_parameters, script)
