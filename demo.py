#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 13 17:46:32 2020

@author: danielbean
"""

## demo use combining structured and free text data

import DrugMentionNLP
from utils import run
import pandas as pd

generic_only = True

drugs = pd.read_csv('data/ace2_drugs.csv')

if generic_only:
    drugs = drugs[drugs['drug'] == drugs['brand name of']]

dr = drugs['drug'].unique().tolist()
print("detecting drugs", dr)

annr = DrugMentionNLP.DrugAnnotator(dr)


#which columns are kept per doc type
docs_keep = ['Patient', 'document_description', 'updatetime']
meds_keep = ['Patient', 'document_description', 'Date']


# =============================================================================
# process free text documents
# =============================================================================
all_docs = pd.read_csv('data/documents.csv')

df = run(annr, all_docs, 'body_analysed', docs_keep)
df = pd.merge(df, drugs, on='drug', how='left')
df.to_csv('data/nlp_docs_all_mentions.csv', index=False)


# =============================================================================
# process structured orders
# =============================================================================
### run NLP on the drug list file
prescriptions = pd.read_csv('data/medication_orders.csv')

df_p = run(annr, prescriptions, 'Order Name', meds_keep)
df_p = pd.merge(df_p, drugs, on='drug', how='left')
df_p.to_csv('data/nlp_prescriptions_all_mentions.csv', index=False)


# =============================================================================
# print some basic counts
# =============================================================================
print("negation status in prescriptions")
print(df_p['negated'].value_counts())
df_p_pos = df_p[df_p['negated'] == False]
#df_p_pos.to_csv('output/all_patients_nlp_prescriptions_pos_mentions.csv', index=False)
gr = df_p_pos.groupby('drug')

print("positive mention count over all", prescriptions.shape[0] ,"prescriptions")
c = gr.size()
print(c)

print("patients with prescriptions")
print(prescriptions['Patient'].nunique())
print("patients with positive mentions in prescriptions")
print(df_p_pos['Patient'].nunique())

    