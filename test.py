from utils import cfg, parse_args, reset_options, GENERAL_CONFIG_OPTIONS, MODEL_OPTIONS, DEFAULT_GENERAL_CONFIG_OPTIONS, DEFAULT_MODEL_OPTIONS, EXTRA_DEFAULTS
from pathlib import Path
import os


def test_all_options():
    test_help_option()
    test_input_options()
    test_output_options()
    test_nocall_option()

def test_help_option():
    assert parse_args(["-h"]) == False
    assert parse_args(["--help"]) == False
    assert parse_args([]) == True
    print ("help flag tests passed")
    
def test_input_options():
    expected1 = {"audio_folder": Path("examples1"), "species_list_file": Path(f"examples1/{EXTRA_DEFAULTS['species_list_file_name']}")}
    test_options("-i examples1", expected1, {})
    test_options("--input_audio examples1", expected1, {})
    expected2 = {"audio_folder": DEFAULT_GENERAL_CONFIG_OPTIONS["audio_folder"], "species_list_file": Path("examples1/species_list_noise1.txt")}
    test_options("-s examples1/species_list_noise1.txt", expected2, {})
    test_options("--species_list examples1/species_list_noise1.txt", expected2, {})
    print ("input file flag tests passed")
    
    
def test_output_options():
    expected1 = {"selection_file_folder": Path("output1"), "combined_output_file": Path(f"output1/{EXTRA_DEFAULTS['combined_output_file_name']}")}
    test_options("-o output1", expected1, {})
    test_options("--output_dir output1", expected1, {})
    expected2 = {"selection_file_folder": DEFAULT_GENERAL_CONFIG_OPTIONS["selection_file_folder"], "combined_output_file": Path("output1/combined_output1.txt")}
    test_options("-c output1/combined_output1.txt", expected2, {})
    test_options("--combined_output output1/combined_output1.txt", expected2, {})
    expected3 = {"combined_output": False, "selection_file_folder": DEFAULT_GENERAL_CONFIG_OPTIONS["selection_file_folder"], "combined_output_file": Path(f"{DEFAULT_GENERAL_CONFIG_OPTIONS['selection_file_folder']}/{EXTRA_DEFAULTS['combined_output_file_name']}")}
    test_options("-p", expected3, {})
    test_options("--separate_only", expected3, {})
    print ("output file flag tests passed")
    

def test_nocall_option():
    expected = {"output_nocall": True}
    test_options("-n", expected, {})
    test_options("--output_nocall", expected, {})
    test_options("", expected, {}, invert = True)
    print ("nocall flag tests passed")


def test_options(options: str, expected_general_results: dict, expected_model_results: dict, invert = False):
    options_list = options.split()
    reset_options()
    parse_args(options_list)
    
    for key in expected_general_results.keys():
        assert (invert != (GENERAL_CONFIG_OPTIONS[key] == expected_general_results[key]))
    
    for key in expected_model_results.keys():
        assert (invert != (MODEL_OPTIONS[key] == expected_model_results[key]))
    
    
if __name__ == "__main__":
    test_all_options()


