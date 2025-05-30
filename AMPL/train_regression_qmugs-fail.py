print ("passing arguments")

import argparse 

parse = argparse.ArgumentParser(description="ForAMPL")
parse.add_argument("-curated_qmug", dest="curated_qmug")
parse.add_argument("-model_dir", dest="model_dir")
#parse.add_argument("-best_model_dir", dest="best_model_dir")

args = parse.parse_args()
print ("importing atomsci")

# importing relevant libraries
import pandas as pd
pd.set_option('display.max_columns', None)
from atomsci.ddm.pipeline import model_pipeline as mp
from atomsci.ddm.pipeline import parameter_parser as parse

# Set up
dataset_file = args.curated_qmug
odir = args.model_dir

response_col = "VALUE_NUM_mean"
compound_id = "compound_id"
smiles_col = "base_rdkit_smiles"

params = {
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
    
        "featurizer": "computed_descriptors",
        "descriptor_type" : "rdkit_raw",
        "model_type": "RF",
        "transformers": "True",
        "rerun": "False",
        "result_dir": odir
    }

ampl_param = parse.wrapper(params)
pl = mp.ModelPipeline(ampl_param)
pl.train_model()