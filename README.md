# Setup Instructions

Here are the instructions for using the pre-alpha prototype version of this program.

Ensure that you have Python 3.11 installed. Python 3.12 ***will not work***.

First, run the `download_model.sh` script. This will fetch the `eBird_taxonomy_codes_2024E.json` file, which is omitted from the git repo due to its size.

If on a Linux (or OSX as well I think?) system, run `setup-venv.sh`. This *should* work, please let me know if it doesn't. This script creates a virtual environment for the python installation and then installs birdnet.



# Usage Instructions

Place all desired input audio files into the `examples` directory. Ensure that all input audio files end in `.WAV` (yes, it's case sensative—this will be fixed in the future). `species_list_noise.txt` *must* remain in the `examples` directory. It should probably be moved later, but for now it's hardcoded to that location.

Run `source activate-bird-venv` to activate the virtual environment in your shell (you should only have to do this once per shell, but if you close the shell or run `deactivate` you will need to run this command again).

Run `python3.11 main.py`


