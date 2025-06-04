#!/bin/bash


if [ ! -f eBird_taxonomy_codes_2024E.json ]; then
	wget https://github.com/birdnet-team/BirdNET-Analyzer/raw/refs/heads/main/birdnet_analyzer/eBird_taxonomy_codes_2024E.json
fi

mkdir V2.4
