from pathlib import Path
import json



    
DEFAULT_MODEL_OPTIONS = {
    "sig_fmin": 0,
    "sig_fmax": 15000,
    "bandpass_fmin": 0,
    "bandpass_fmax": 15000,
    "audio_speed": 1.0,
}

TYPE_CASTING_FUNCTIONS = {
    "int": lambda x: int(x),
    "float": lambda x: float(x),
    "str": lambda x: x,
}


MODEL_OPTIONS = DEFAULT_MODEL_OPTIONS.copy()

def model_option(option_name: str): 
    return property(
            fget=lambda x: MODEL_OPTIONS[option_name],
            fset=lambda x, val: MODEL_OPTIONS.update({option_name: val}),
            fdel=lambda x: MODEL_OPTIONS.update({option_name: DEFAULT_MODEL_OPTIONS[option_name]}),
        )
    
class Cfg:
    # Frequency range. This is model specific and should not be changed.
    SIG_FMIN: int = model_option("sig_fmin")
    SIG_FMAX: int = model_option("sig_fmax")
    # Settings for bandpass filter
    BANDPASS_FMIN: int = model_option("bandpass_fmin")
    BANDPASS_FMAX: int = model_option("bandpass_fmax")

    # Audio speed
    AUDIO_SPEED: float = model_option("audio_speed")
    
    _options_list = map(lambda opt: f"--{opt}", MODEL_OPTIONS.keys())
    
    def get_options_desc(self):
        return map(lambda opt: f"{opt}=", MODEL_OPTIONS.keys())
    
    def get_options_list(self):
        return self._options_list
        
    def set_option(self, opt, arg):
        """This function sets a config option. The reason it's so cursed is because it automatically 
        converts whatever input string it's given into the correct type for that config option, by matching
        the type of the option's default value. Currently only int, float, and str types are supported.
        
        It is likely that support for booleans will be added, as this system will likely be expanded in the future."""
        o = opt[2:]
        type_info = type(MODEL_OPTIONS[o])
        type_name = f"{type_info}"[8:-2]
        MODEL_OPTIONS[o]=TYPE_CASTING_FUNCTIONS[type_name](arg)

cfg = Cfg()






def read_lines(path: str | Path):
    """Reads the lines into a list.

    Opens the file and reads its contents into a list.
    It is expected to have one line for each species or label.

    Args:
        path: Absolute path to the species file.

    Returns:
        A list of all species inside the file.
    """
    return Path(path).read_text(encoding="utf-8").splitlines() if path else []
    
def load_codes(codes_file):
    """Loads the eBird codes.

    Returns:
        A dictionary containing the eBird codes.
    """
    with open(codes_file) as cfile:
        return json.load(cfile)