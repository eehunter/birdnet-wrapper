from pathlib import Path
from birdnet import SpeciesPredictions, predict_species_within_audio_file, predict_species_at_location_and_time, get_species_from_file
import librosa
import os
import utils

# Disables a bunch of unimportant warnings that make it hard to view the actual output
import absl.logging
absl.logging.set_verbosity(absl.logging.ERROR)

# Program input settings. Should be replaced with CLI args later, probably
audio_folder = Path("examples")
species_list_file = Path("examples/species_list_noise.txt")
selection_file_folder = Path("output")
output_nocall = False


RAVEN_TABLE_HEADER = (
    "Selection\tView\tChannel\tBegin Time (s)\tEnd Time (s)\tLow Freq (Hz)\tHigh Freq (Hz)\tCommon Name\tSpecies Code\tConfidence\tBegin Path\tFile Offset (s)\n"
)
SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
CODES_FILE: str = os.path.join(SCRIPT_DIR, "eBird_taxonomy_codes_2024E.json")
LABELS_FILE: str = os.path.join(SCRIPT_DIR, "V2.4/BirdNET_GLOBAL_6K_V2.4_Labels.txt")
TRANSLATED_LABELS_PATH: str = os.path.join(SCRIPT_DIR, "labels/V2.4")



LABELS = utils.read_lines(LABELS_FILE)
CODES = utils.load_codes(CODES_FILE)

# Frequency range. This is model specific and should not be changed.
SIG_FMIN: int = 0
SIG_FMAX: int = 15000

# Settings for bandpass filter
BANDPASS_FMIN: int = 0
BANDPASS_FMAX: int = 15000

# Audio speed
AUDIO_SPEED: float = 1.0


species_list = set("")
with open(species_list_file, 'r') as file:
    species_list = set(file.read().splitlines(True))
    


def predict_species_for_file(file: Path):
    predictions = SpeciesPredictions(predict_species_within_audio_file(
        file,
        min_confidence=0.3,
        sigmoid_sensitivity=1.5,
        species_filter=get_species_from_file(species_list_file)
    ))
    
    

    # get most probable prediction at time interval 0s-3s
    
    timestamps = []
    result = {}
    
    
    for timestamp, prediction in predictions.items():
        if not bool(prediction):
            continue
        print(prediction.items())
        timestamp_str = f"{timestamp[0]}-{timestamp[1]}"
        timestamps.append(timestamp_str)
        result[timestamp_str] = prediction.items()
        # if not timestamp_str in result.keys():
        #     result[timestamp_str] = []
        # result[timestamp_str].append(prediction)
        
    generate_raven_table(timestamps, result, file, get_result_file_name(file))
    
    
    # prediction, confidence = list(predictions[(0.0, 3.0)].items())[0]
    # print(f"predicted '{prediction}' with a confidence of {confidence:.6f}")
    # predicted 'Poecile atricapillus_Black-capped Chickadee' with a confidence of 0.814056





def get_result_file_name(fpath: str | Path):
    """
    Generates a dictionary of result file names based on the input file path and configured result types.

    Args:
        fpath (str): The file path of the input file.

    Returns:
        dict: A dictionary where the keys are result types (e.g., "table", "audacity", "r", "kaleidoscope", "csv")
              and the values are the corresponding output file paths.
    """
    result_names = {}

    rpath = str(fpath).replace(str(audio_folder), "")

    rpath = (rpath[1:] if rpath[0] in ["/", "\\"] else rpath) if rpath else os.path.basename(fpath)

    file_shorthand = rpath.rsplit(".", 1)[0]

    return os.path.join(str(selection_file_folder), file_shorthand + ".BirdNET.selection.table.txt")
    
def generate_raven_table(timestamps: list[str], result: dict[str, list], afile_path: str, result_path: str):
    """
    Generates a Raven selection table from the given timestamps and prediction results.

    Args:
        timestamps (list[str]): List of timestamp strings in the format "start-end".
        result (dict[str, list]): Dictionary where keys are timestamp strings and values are lists of predictions.
        afile_path (str): Path to the audio file being analyzed.
        result_path (str): Path where the resulting Raven selection table will be saved.

    Returns:
        None
    """
    selection_id = 0
    out_string = ""

    # Read native sample rate
    high_freq = librosa.get_samplerate(afile_path) / 2

    high_freq = min(high_freq, int(SIG_FMAX / AUDIO_SPEED))

    high_freq = int(min(high_freq, int(BANDPASS_FMAX / AUDIO_SPEED)))
    low_freq = max(SIG_FMIN, int(BANDPASS_FMIN / AUDIO_SPEED))

    # Extract valid predictions for every timestamp
    for timestamp in timestamps:
        rstring = ""
        start, end = timestamp.split("-", 1)

        for c in result[timestamp]:
            selection_id += 1
            label = c[0]#TRANSLATED_LABELS[LABELS.index(c[0])]
            code = CODES[c[0]] if c[0] in CODES else c[0]
            rstring += (
                f"{selection_id}\tSpectrogram 1\t1\t{start}\t{end}\t{low_freq}\t{high_freq}\t{label.split('_', 1)[-1]}\t{code}\t{c[1]:.4f}\t{afile_path}\t{start}\n"
            )

        
        # Write result string to file
        out_string += rstring

    # If we don't have any valid predictions, we still need to add a line to the selection table
    # in case we want to combine results
    # TODO: That's a weird way to do it, but it works for now. It would be better to keep track
    # of file durations during the analysis.
    nocall = len(out_string) == 0
    if nocall:
        if output_nocall:
            selection_id += 1
            out_string += f"{selection_id}\tSpectrogram 1\t1\t0\t3\t{low_freq}\t{high_freq}\tnocall\tnocall\t1.0\t{afile_path}\t0\n"
        else:
            return

    save_result_file(result_path, out_string, nocall)
    


def save_result_file(result_path: str, out_string: str, nocall: bool):
    """Saves the result to a file.

    Args:
        result_path: The path to the result file.
        out_string: The string to be written to the file.
    """

    # Make directory if it doesn't exist
    os.makedirs(os.path.dirname(result_path), exist_ok=True)

    # Write the result to the file
    with open(result_path, "w", encoding="utf-8") as rfile:
        rfile.write(RAVEN_TABLE_HEADER+out_string)
    if nocall: return
    with open(os.path.join(selection_file_folder, "combined_output.txt"), "a", encoding="utf-8") as rfile:
        rfile.write(out_string)


with open(os.path.join(selection_file_folder, "combined_output.txt"), "w", encoding="utf-8") as rfile:
    rfile.write(RAVEN_TABLE_HEADER)


audio_files = audio_folder.glob("*.WAV")
for path in audio_files:
    predict_species_for_file(path)
