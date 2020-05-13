#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 13 18:07:59 2020

@author: danielbean
"""

import pandas as pd

## basic function to handle formatting output

def run(annr, docs_df, doc_col, keep_cols):
    all_results = {}
    i = 0
    for index, row in docs_df.iterrows():
        doc = row[doc_col]
        #doc = doc.encode('utf8')
        result = annr.annotate(doc)
        result['meta'] = {}
        for k in keep_cols:
            result['meta'][k] = row[k]
        did = 'doc_' + str(i)
        result['meta']['doc_id'] = did
        all_results[did] = result
        i += 1
        
    #reformat
    rows = []
    keep = keep_cols
    for doc_id in all_results:
        anns = all_results[doc_id]
        if len(anns['mentions']) > 0:
            for m in anns['mentions']:
                for k in keep:
                    m[k] = anns['meta'][k]
                rows.append(m)
    df = pd.DataFrame(rows)
    return df