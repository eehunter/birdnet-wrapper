from pathlib import Path
import json
import sys, getopt


# Default settings. Must be declaired at top-level for now. 
# These may eventually be abstracted to an object in the utils file,
# as this would prevent possible issues with unit tests if any of these values
# are changed here without also being changed in the reset_options function.
audio_folder = Path("examples")
species_list_file = None 
selection_file_folder = Path("output")

output_nocall = False

combined_output = True
combined_output_file = None 

overwrite_files = False

def reset_options():
    """Used for unit testing."""
    audio_folder = Path("examples")
    species_list_file = None 
    selection_file_folder = Path("output")

    output_nocall = False

    combined_output = True
    combined_output_file = None 

    overwrite_files = False
    
    reset_model_options()
    
def parse_args(args):
    """Parses command line options/arguments for program."""
    try:
        opts, args = getopt.getopt(args,"i:s:o:c:nph", ["input_audio=","species_list=","output_dir=","combined_output=","output_nocall","separate_only","overwrite_files","help",*cfg.get_options_desc()])
    except getopt.GetoptError:
        print("main.py [-i <input_audio_directory>] [-s <species_list_file>] [-o <output_directory>] [-c <combined_output_file>] [-n]")
        print("""Run "main.py -h" for a list of options.""")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', "--help"):
            print("""Usage:
        -h, --help :            Show this message.
        -i, --input_audio:      Choose a folder to input audio files from.
        -s, --species_list:     Choose species list file.
        -o, --output_dir:       Choose directory for individual output files.
        -c, --combined_output:  Choose path to combined output file.""")
            sys.exit(0) 
        if opt in ('-i', "--input_audio"):
            audio_folder = Path(arg)
        if opt in ('-s', "--species_list"):
            species_list_file = Path(arg)
        if opt in ('-o', "--output_dir"):
            selection_file_folder = Path(arg)
        if opt in ('-c', "--combined_output"):
            combined_output_file = Path(arg)
        if opt in ('-p', "--separate_only"):
            combined_output = False
        if opt in ('-n', "--output_nocall"):
            output_nocall = True
        if opt == "--overwrite_files":
            overwrite_files = True
        if opt in cfg.get_options_list():
            cfg.set_option(opt, arg)
        
    if species_list_file is None:
        species_list_file = Path(os.path.join(audio_folder, "species_list_noise.txt"))

    if combined_output_file is None:
        combined_output_file = Path(os.path.join(selection_file_folder, "combined_output.txt"))

    
DEFAULT_MODEL_OPTIONS = {
    "sig_fmin": 0,
    "sig_fmax": 15000,
    "bandpass_fmin": 0,
    "bandpass_fmax": 15000,
    "audio_speed": 1.0,
    "min_confidence": 0.3,
    "sigmoid_sensitivity": 0.5,
    "chunk_overlap": 2.0,
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
    
    # Minimum Confidence
    MIN_CONFIDENCE: float = model_option("min_confidence")
    
    # Sigmoid Sensativity
    SIG_SENSE: float = model_option("sigmoid_sensitivity")
    
    # Chunk Overlap (Seconds)
    CHUNK_OVERLAP: float = model_option("chunk_overlap")
    
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


def reset_model_options():
    """This function is used for unit testing."""
    MODEL_OPTIONS = DEFAULT_MODEL_OPTIONS.copy()



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