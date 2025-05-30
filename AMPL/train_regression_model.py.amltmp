print ("passing arguments")

import argparse 

parse = argparse.ArgumentParser(description="ForAMPL")
parse.add_argument("-curated_qmug", dest="curated_qmug")
parse.add_argument("-odir", dest="odir")
parse.add_argument("-final", dest="final")

args = parse.parse_args()


# importing relevant libraries
import pandas as pd
from atomsci.ddm.pipeline import model_pipeline as mp
from atomsci.ddm.pipeline import parameter_parser as parse
print ("importing atomsci")
# Set up
dataset_file = args.curated_qmug
odir = args.odir


import os
import shutil

# Define the path for the /temp directory
temp_dir = "/temp"

# Create the /temp directory if it doesn't exist
os.makedirs(temp_dir, exist_ok=True)

# Load the curated dataset
curated_dataset = args.curated_qmug

# Print the current path of curated_dataset
print(f"Original dataset path: {curated_dataset}")

# Get just the filename of the dataset
dataset_filename = os.path.basename(curated_dataset)

# Define the path for the copied dataset in the /temp directory
temp_dataset_path = os.path.join(temp_dir, dataset_filename)

# Print the new path
print(f"New dataset path: {temp_dataset_path}")

# Check if the paths are different before copying
if curated_dataset != temp_dataset_path:
    # Copy the curated dataset to the /temp directory
    shutil.copy2(curated_dataset, temp_dataset_path)
    print(f"Dataset copied to: {temp_dataset_path}")
else:
    print("Source and destination are the same. No copy needed.")

# Update the dataset_file variable to use the new path
dataset_file = temp_dataset_path


response_col = "VALUE_NUM_mean"
compound_id = "compound_id"
smiles_col = "base_rdkit_smiles"


params = {
        "verbose": "True",
        "prediction_type": "regression",
        "dataset_key": dataset_file,
        "id_col": compound_id,
        "smiles_col": smiles_col,
        "response_cols": response_col,
    
        "previously_split": "False",
        "split_only": "False",
        "splitter": "scaffold",
        "split_valid_frac": "0.15",
        "split_test_frac": "0.15",
    
        "featurizer": "graphconv",
 #       "descriptor_type" : "rdkit_raw",
        "model_type": "NN",
        "transformers": "True",
        "rerun": "False",
        "result_dir": odir
    }

ampl_param = parse.wrapper(params)
pl = mp.ModelPipeline(ampl_param)

pl.train_model()

print ("model trained")

# display the split file location
import glob
import os

output_dir = args.final

# Copy files and directories
for item in os.listdir(temp_dir):
    src_path = os.path.join(temp_dir, item)
    dst_path = os.path.join(output_dir, item)
    if os.path.isdir(src_path):
        shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
    else:
        shutil.copy2(src_path, dst_path)

print("done")

