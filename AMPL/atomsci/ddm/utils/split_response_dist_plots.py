"""Module to plot distributions of response values in each subset of a dataset generated by a split"""

import os
import numpy as np
import pandas as pd
from atomsci.ddm.pipeline import parameter_parser as parse

import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats


# ---------------------------------------------------------------------------------------------------------------------------------
def plot_split_subset_response_distrs(params, axes=None, plot_size=7):
    """Plot the distributions of the response variable(s) in each split subset of a dataset.
    
    Args:
        params (argparse.Namespace or dict): Structure containing dataset and split parameters.
        The following parameters are required, if not set to default values:
        
        | - dataset_key
        | - split_uuid
        | - split_strategy
        | - splitter
        | - split_valid_frac
        | - split_test_frac
        | - num_folds
        | - smiles_col
        | - response_cols

        axes (matplotlib.Axes): Axes to draw plots in, if provided
        plot_size (float): Height of plots; ignored if axes is provided
    Returns:
        None
    """

    # Save current matplotlib color cycle and switch to 'colorblind' palette
    old_palette = sns.color_palette()
    sns.set_palette('colorblind')

    if isinstance(params, dict):
        params = parse.wrapper(params)
    dset_df, split_label = get_split_labeled_dataset(params)
    if params.split_strategy == 'k_fold_cv':
        subset_order = sorted(set(dset_df.split_subset.values))
    else:
        subset_order = ['train', 'valid', 'test']

    wdist_df = compute_split_subset_wasserstein_distances(params)


    if axes is None:
        fig, axes = plt.subplots(1, len(params.response_cols), figsize=(plot_size*len(params.response_cols), plot_size))
    if len(params.response_cols) == 1:
        axes = [axes]
    else:
        axes = axes.flatten()
    for colnum, col in enumerate(params.response_cols):
        ax = axes[colnum]
        if params.split_strategy == 'train_valid_test':
            tvv_wdist = wdist_df[(wdist_df.split_subset == 'valid') & (wdist_df.response_col == col)].distance.values[0]
            tvt_wdist = wdist_df[(wdist_df.split_subset == 'test') & (wdist_df.response_col == col)].distance.values[0]
        if params.prediction_type == 'regression':
            ax = sns.kdeplot(data=dset_df, x=col, hue='split_subset', hue_order=subset_order, 
                             bw_adjust=0.7, fill=True, common_norm=False, ax=ax)
            ax.set_title(f"{col} distribution by subset under {split_label}")
            if params.split_strategy == 'train_valid_test':
                ax.set_title(f"{col} distribution by subset under {split_label}\n" \
                             f"Wasserstein distances: valid = {tvv_wdist:.3f}, test = {tvt_wdist:.3f}")
            else:
                ax.set_title(f"{col} distribution by subset under {split_label}")
        else:
            pct_active = []
            for ss in subset_order:
                ss_df = dset_df[dset_df.split_subset == ss]
                nactive = np.nansum(ss_df[col].values)
                pct_active.append(100*nactive/sum(ss_df[col].notna()))
            active_df = pd.DataFrame(dict(subset=subset_order, percent_active=pct_active))
            ax = sns.barplot(data=active_df, x='subset', y='percent_active', hue='subset', ax=ax)

            if params.split_strategy == 'train_valid_test':
                ax.set_title(f"Percent of {col} = 1 by subset under {split_label}" \
                             f"Wasserstein distances: valid = {tvv_wdist:.3f}, test = {tvt_wdist:.3f}")
            else:
                ax.set_title(f"Percent of {col} = 1 by subset under {split_label}")
            ax.set_xlabel('')

    # Restore previous matplotlib color cycle
    sns.set_palette(old_palette)

# ---------------------------------------------------------------------------------------------------------------------------------
def compute_split_subset_wasserstein_distances(params):
    """Compute the Wasserstein ("earth-moving") distance between the distributions of the response variable(s) in the validation
    and test sets to that of the training set. In the case of a k-fold CV split, compare the distributions of folds 1 through k-1
    and the test set to that of fold 0.
    
    Args:
        params (argparse.Namespace or dict): Structure containing dataset and split parameters.
        The following parameters are required, if not set to default values:
        
        | - dataset_key
        | - split_uuid
        | - split_strategy
        | - splitter
        | - split_valid_frac
        | - split_test_frac
        | - num_folds
        | - smiles_col
        | - response_cols

    Returns:
        (DataFrame): A table of Wasserstein distances relative to the training set or fold 0 for each other split subset, for each
        response variable.
    """

    if isinstance(params, dict):
        params = parse.wrapper(params)
    dset_df, split_label = get_split_labeled_dataset(params)
    if params.split_strategy == 'k_fold_cv':
        subset_order = sorted(set(dset_df.split_subset.values))
    else:
        subset_order = ['train', 'valid', 'test']

    response_vars = []
    subsets = []
    distances = []
    train_set = subset_order[0]
    for col in params.response_cols:
        train_vals = dset_df[dset_df.split_subset == train_set][col].values
        train_vals = train_vals[~np.isnan(train_vals)]
        for subset in subset_order[1:]:
            subset_vals = dset_df[dset_df.split_subset == subset][col].values
            subset_vals = subset_vals[~np.isnan(subset_vals)]
            dist = stats.wasserstein_distance(train_vals, subset_vals)
            response_vars.append(col)
            subsets.append(subset)
            distances.append(dist)
    dist_df = pd.DataFrame(dict(response_col=response_vars, split_subset=subsets, distance=distances))
    return dist_df


# ---------------------------------------------------------------------------------------------------------------------------------
def get_split_labeled_dataset(params):
    """Add a column to a dataset labeling the split subset for each row.
    Given a dataset and split parameters (including split_uuid) referenced in `params`, returns a data frame
    containing the dataset with an extra 'split_subset' column indicating the subset each data point belongs to.
    For standard 3-way splits, the labels will be 'train', 'valid' and 'test'. For a k-fold CV split, the labels will 
    be 'fold_0' through 'fold_<k-1>' and 'test'.

    Args:
        params (argparse.Namespace or dict): Structure containing dataset and split parameters.
        The following parameters are required, if not set to default values:
        
        | - dataset_key
        | - split_uuid
        | - split_strategy
        | - splitter
        | - split_valid_frac
        | - split_test_frac
        | - num_folds
        | - smiles_col
        | - response_cols

    Returns:
        A tuple (dset_df, split_label):
        
        | - dset_df (DataFrame): The dataset specified by `params.dataset_key`, with additional column `split_subset`.
        | - split_label (str): A short description of the split, useful for plot labeling.
    """
    if isinstance(params, dict):
        params = parse.wrapper(params)
    dset_df = pd.read_csv(params.dataset_key, dtype={params.id_col: str})
    if params.split_strategy == 'k_fold_cv':
        split_file = f"{os.path.splitext(params.dataset_key)[0]}_{params.num_folds}_fold_cv_{params.splitter}_{params.split_uuid}.csv"
    else:
        split_file = f"{os.path.splitext(params.dataset_key)[0]}_{params.split_strategy}_{params.splitter}_{params.split_uuid}.csv"
    split_df = pd.read_csv(split_file, dtype={'cmpd_id': str}).rename(columns={'cmpd_id': 'compound_id'})
    dset_df = dset_df.merge(split_df, how='left', on='compound_id')
    if params.split_strategy == 'k_fold_cv':
        dset_df['split_subset'] = [f"fold_{f}" for f in dset_df.fold.values]
        dset_df.loc[dset_df.subset == 'test', 'split_subset'] = 'test'
        nfolds = max(dset_df.fold.values) + 1
        split_label = f"{nfolds}-fold {params.splitter} cross-validation split"
    else:
        dset_df['split_subset'] = dset_df.subset.values
        if params.splitter == 'multitaskscaffold':
            split_label = 'MTSS split'
        else:
            split_label = f"{params.splitter} split"
    return dset_df, split_label

