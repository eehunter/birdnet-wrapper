# Setup Instructions

Here are the instructions for using the pre-alpha prototype version of this program.

Ensure that you have Python 3.11 installed. Python 3.12 ***will not work***.

First, run the `download_model.sh` script. This will fetch the `eBird_taxonomy_codes_2024E.json` file, which is omitted from the git repo due to its size.

If on a Linux (or OSX as well I think?) system, run `setup-venv.sh`. This *should* work, please let me know if it doesn't. This script creates a virtual environment for the python installation and then installs birdnet.



# Usage Instructions

## Linux

Place all desired input audio files in an input directory. By default, `./examples/` is used. This can be changed 
with the `-i` or `--input_audio` commandline options.

Input files must be in wav format and have a `.wav` extension. The input directory will be recursively scanned for 
wav files.

A species list file must be provided. By default, this is set to a file called `species_list_noise.txt` within the 
input directory. This can be changed with `-s` or `--species_list`. *Note that while the default value is relative 
to the input directory, a custom value is relative to the directory that the application is running in.*

Output files are written to a directory called `./output/` by default. This can be changed with `-o` or 
`--output_dir`. 

To begin, create a virtual python environment using the following command. You may substitute `python3.11` for a path to a valid Python 3.11 executable.

```virtualenv bird-venv --python=python3.11```

Next, activate the virtual environment in your shell. This will have to be done every time you try to run the program in a new shell.

```source ./bird-venv/bin/activate```

In a shell with the virtual environment active, run one of the two following commands. Use the first one if you would like to run BirdNET on your CPU only, and the second if you plan to use a GPU as well. Only Nvidia GPUs with official drivers and CUDA installed are supported. (The commands are from the BirdNET README. I haven't tested the second one, as I don't have a dedicated GPU on this computer)

```pip install birdnet --user```

```pip install birdnet[and-cuda] --user```

Now you can run the program with the following command. You may need to replace `python3.11` with `python3`, depending on your python installation. Program args may be added to this command.

```python3.11 main.py```

For more info on commandline arguments, run 

```python3.11 main.py -h```



## Old Instructions (Deprecated)

Place all desired input audio files into the `examples` directory. Ensure that all input audio files end in `.WAV` (yes, it's case sensative—this will be fixed in the future). `species_list_noise.txt` *must* remain in the `examples` directory. It should probably be moved later, but for now it's hardcoded to that location.

Run `source activate-bird-venv` to activate the virtual environment in your shell (you should only have to do this once per shell, but if you close the shell or run `deactivate` you will need to run this command again).

Run `python3.11 main.py`


