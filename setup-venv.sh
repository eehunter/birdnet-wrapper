
# Setup venv. You should probably ignore this if not on linux or OSX.
virtualenv bird-venv --python=python3.11

ln -s ./bird-venv/bin/activate ./activate-bird-venv

source activate-bird-venv

python3.11 -m pip install birdnet