print ("passing arguments")

import argparse 

parse = argparse.ArgumentParser(description="ForAMPL")
parse.add_argument("-curated_qmug", dest="curated_qmug")
parse.add_argument("-odir", dest="odir")

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
   # "system": "LC",

    # dataset info
    "dataset_key" : dataset_file,
    "datastore": "False",
    "response_cols" : response_col,
    "id_col": compound_id,
    "smiles_col" : smiles_col,
    "result_dir": odir,

    # splitting
    "split_only": "True",
    "previously_split": "False",
    "splitter": 'scaffold',
    "split_valid_frac": "0.15",
    "split_test_frac": "0.15",

    # featurization & training params
    "featurizer": "ecfp",
    #"descriptor_type" : "rdkit_raw",
    "previously_featurized": "True",
}

pparams = parse.wrapper(params)
MP = mp.ModelPipeline(pparams)
split_uuid = MP.split_dataset()
print ("dataset split")

# display the split file location
import glob
import os


# Display the split file location
split_file = glob.glob(f"{temp_dir}/*{split_uuid}*")[0]
print(f"Split file in temp: {split_file}")

# Define the path for the output file in the original directory
output_file = os.path.join(odir, os.path.basename(split_file))

# Copy the split file back to the original output directory
shutil.copy2(split_file, output_file)
print(f"Split file copied to: {output_file}")

print("done")
