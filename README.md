# Setup and Usage Instructions

## Linux / MacOS

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

```bash
virtualenv bird-venv --python=python3.11
```

Next, activate the virtual environment in your shell. This will have to be done every time you try to run the program in a new shell.

```bash
source ./bird-venv/bin/activate
```

In a shell with the virtual environment active, run one of the two following commands. Use the first one if you would like to run BirdNET on your CPU only, and the second if you plan to use a GPU as well. Only Nvidia GPUs with official drivers and CUDA installed are supported. (The commands are from the BirdNET README. I haven't tested the second one, as I don't have a dedicated GPU on this computer)

```bash
python3.11 -m pip install birdnet 
```

```bash 
python3.11 -m pip install birdnet[and-cuda] 
```

Finally, you must download the taxonomy codes file with one of the following commands, depending on your OS.

```bash
# Linux
wget https://github.com/birdnet-team/BirdNET-Analyzer/raw/refs/heads/main/birdnet_analyzer/eBird_taxonomy_codes_2024E.json

# MacOS
curl https://github.com/birdnet-team/BirdNET-Analyzer/raw/refs/heads/main/birdnet_analyzer/eBird_taxonomy_codes_2024E.json -o eBird_taxonomy_codes_2024E.json
```

Now you can run the program with the following command. You may need to replace `python3.11` with `python3`, depending on your python installation. Program args may be added to this command.

```bash
python3.11 main.py
```

For more info on commandline arguments, run 

```bash
python3.11 main.py -h
```

## Windows

Place all desired input audio files in an input directory. By default, `.\examples\` is used. This can be changed 
with the `-i` or `--input_audio` commandline options.

Input files must be in wav format and have a `.wav` extension. The input directory will be recursively scanned for 
wav files.

A species list file must be provided. By default, this is set to a file called `species_list_noise.txt` within the 
input directory. This can be changed with `-s` or `--species_list`. *Note that while the default value is relative 
to the input directory, a custom value is relative to the directory that the application is running in.*

Output files are written to a directory called `.\output\` by default. This can be changed with `-o` or 
`--output_dir`. 

To begin, create a virtual python environment using the following command in a cmd or PowerShell window. You may substitute `python3.11` for a path to a valid Python 3.11 executable. You may need to replace `python` with `python3` or `python3.11`, depending on how your Python installation is configured.

```python -m venv bird-venv --python=python3.11```

Next, activate the virtual environment with one of the following commands.

```bat
::cmd.exe
bird-venv\Scripts\activate.bat

::PowerShell
bird-venv\Scripts\Activate.ps1
```

If you used the second option, you may have to run this command in PowerShell. I don't really know what it does, but the venv documentation says it might be required. More info can be found [here](https://go.microsoft.com/fwlink/?LinkID=135170).

```Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser```

In a shell with the virtual environment active, run one of the two following commands. Use the first one if you would like to run BirdNET on your CPU only, and the second if you plan to use a GPU as well. Only Nvidia GPUs with official drivers and CUDA installed are supported. (The commands are from the BirdNET README. I haven't tested the second one, as I don't have a dedicated GPU on this computer)

```bat
python3.11 -m pip install birdnet --user
```

```bat 
python3.11 -m pip install birdnet[and-cuda] --user
```

Finally, you must download the taxonomy codes file. The following two commands should download it in a PowerShell window. If that doesn't work, you can download the file [here](https://github.com/birdnet-team/BirdNET-Analyzer/raw/refs/heads/main/birdnet_analyzer/eBird_taxonomy_codes_2024E.json).

```bat
client = new-object System.Net.WebClient
client.DownloadFile("https://github.com/birdnet-team/BirdNET-Analyzer/raw/refs/heads/main/birdnet_analyzer/eBird_taxonomy_codes_2024E.json",".\eBird_taxonomy_codes_2024E.json")
```

Now, with your virtual environment active, you can run the program with the following command. You may need to replace `python3.11` with `python3`, depending on your python installation. Program args may be added to this command.

```bat
python3.11 main.py
```

For more info on commandline arguments, run 

```bat
python3.11 main.py -h
```
