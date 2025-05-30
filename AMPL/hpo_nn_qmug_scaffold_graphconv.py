import argparse 


parse = argparse.ArgumentParser(description="ForAMPL")
parse.add_argument("-curated_qmug", dest="curated_qmug")
parse.add_argument("-model_dir", dest="model_dir")
parse.add_argument("-best_model_dir", dest="best_model_dir")

args = parse.parse_args()

print("starting HPO")


import warnings
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=RuntimeWarning)

import os

dataset_key = args.curated_qmug
#descriptor_type = 'rdkit_raw'
model_dir = args.model_dir
best_model_dir = args.best_model_dir
#split_uuid = '0a2b3033-05a2-475e-bcd4-fa7c81329f3b'


#if not os.path.exists(f'./{best_model_dir}'):
 #   os.mkdir(f'./{best_model_dir}')
    
#if not os.path.exists(f'./{model_dir}'):
 #   os.mkdir(f'./{model_dir}')
    
print("parameters set")


    
params = {
    "hyperparam": "True",
    "prediction_type": "regression",

    "dataset_key": dataset_key,
    "id_col": "compound_id",
    "smiles_col": "base_rdkit_smiles",
    "response_cols": "VALUE_NUM_mean",

    "splitter":"scaffold",
  #  "split_uuid": split_uuid,
    "previously_split": "False",

    "featurizer": "graphconv",
  #  "descriptor_type" : descriptor_type,
    "transformers": "True",

    ### Use a NN model
    "search_type": "hyperopt",
    "model_type": "NN|10",
    "lr": "loguniform|-13.8,-3",
    "ls": "uniformint|3|8,512",
    "dp": "uniform|3|0,0.4",
    "max_epochs":10,
    ###


    "result_dir": f"./{best_model_dir},./{model_dir}"
}

print ("parameters added")

import atomsci.ddm.utils.hyperparam_search_wrapper as hsw
import importlib
importlib.reload(hsw)
ampl_param = hsw.parse_params(params)
hs = hsw.build_search(ampl_param)
hs.run_search()

print ("starting compare models")
import atomsci.ddm.pipeline.compare_models as cm

result_df = cm.get_filesystem_perf_results(
    result_dir=model_dir,
    pred_type='regression'
)


print ("sorting by r2")
# sort by validation r2 score to see top performing models
result_df = result_df.sort_values(by='best_valid_r2_score', ascending=False)
result_df[['model_uuid','model_parameters_dict','best_valid_r2_score','best_test_r2_score']].head()