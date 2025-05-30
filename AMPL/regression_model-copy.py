print ("passing arguments")

import argparse 

parse = argparse.ArgumentParser(description="ForAMPL")
parse.add_argument("-curated_qmug", dest="curated_qmug")
parse.add_argument("-model_dir", dest="model_dir")
parse.add_argument("-best_model_dir", dest="best_model_dir")
parse.add_argument("-split_uuid", dest="split_uuid")

args = parse.parse_args()
print ("importing atomsci")

# importing relevant libraries
import pandas as pd
from atomsci.ddm.pipeline import model_pipeline as mp
from atomsci.ddm.pipeline import parameter_parser as parse
curated_dataset = args.curated_qmug

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


#creating temp directory

#import tempfile
#import os
#import shutil
# Create a temporary directory
#temp_dir = tempfile.mkdtemp()

# Save the curated dataset to the temporary directory
#temp_dataset_path = os.path.join(temp_dir, "qmugs_curated_160_dropped_duplicates.csv")
#curated_dataset.to_csv(temp_dataset_path, index=False)

# Update the dataset_file variable to use the temporary path
#dataset_file = temp_dataset_path



# Set up
#dataset_file = args.curated_qmug("qmugs_curated_160_dropped_duplicates.csv")
#descriptor_type = 'rdkit_raw'
odir = args.model_dir
#best_model_dir = args.best_model_dir


response_col = "VALUE_NUM_mean"
compound_id = "compound_id"
smiles_col = "base_rdkit_smiles"
split_uuid = "1bc01160-9bde-49d0-b7b6-d07e5c0af747"

params = {
        "verbose": "True",
        "system": "LC",
        "datastore": "False",
        "save_results": "False",
        "prediction_type": "regression",
        "dataset_key": dataset_file,
        "id_col": compound_id,
        "smiles_col": smiles_col,
        "response_cols": response_col,
    
        "previously_split": "True",
        "split_uuid" : split_uuid,
        "split_only": "False",
        "splitter": "scaffold",
        "split_valid_frac": "0.15",
        "split_test_frac": "0.15",
    
        "featurizer": "ecfp",
      #  "descriptor_type" : "rdkit_raw",
        "model_type": "RF",
        "verbose": "True",
        "transformers": "True",
        "rerun": "False",
        "result_dir": odir
    }


ampl_param = parse.wrapper(params)

print ("parameters set")

pl = mp.ModelPipeline(ampl_param)
pl.train_model()

print ("model trained")

print ("done")
