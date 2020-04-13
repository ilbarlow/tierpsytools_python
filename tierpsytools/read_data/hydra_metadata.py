#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 15:52:14 2020

@author: em812
"""

import pandas as pd

def imgstore_name_from_filename(filename, path_levels=[-3,-1]):
    from pathlib import Path

    imgstore_name = '/'.join(Path(filename).parts[path_levels[0]:path_levels[1]])
    return imgstore_name


def read_hydra_metadata(feat, fname, meta, feat_id_cols = ['file_id', 'well_name', 'is_good_well']):

    if 'filename' in fname:
        filename = 'filename'
    elif 'file_name' in fname:
        filename = 'file_name'
    else:
        raise ValueError('The filenames dataframe needs to have a filename column.')

    fname['imgstore_name'] = fname[filename].apply(lambda x: imgstore_name_from_filename(x,path_levels=[-3,-1]))

    newmeta = feat[feat_id_cols]

    newmeta.insert(0,'imgstore_name',newmeta['file_id'].map(dict(fname[['file_id', 'imgstore_name']].values)))

    newmeta = pd.merge(newmeta, meta, on=['imgstore_name','well_name'], how='left')

    assert newmeta.shape[0] == feat.shape[0]

    return feat[feat.columns.difference(feat_id_cols)], newmeta