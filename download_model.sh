#!/bin/bash


if [ ! -f eBird_taxonomy_codes_2024E.json ]; then
	if [[ "$OSTYPE" == "linux-gnu"* ]]; then
		wget https://github.com/birdnet-team/BirdNET-Analyzer/raw/refs/heads/main/birdnet_analyzer/eBird_taxonomy_codes_2024E.json
	elif [[ "$OSTYPE" == "darwin"* ]]; then
		curl https://github.com/birdnet-team/BirdNET-Analyzer/raw/refs/heads/main/birdnet_analyzer/eBird_taxonomy_codes_2024E.json -o eBird_taxonomy_codes_2024E.json
	fi
fi

mkdir V2.4
