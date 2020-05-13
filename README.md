# DrugPipeline

Modified from https://github.com/CogStack/OAC-NLP

data/ace2_drugs.csv is the list of drugs used for our preprint [Treatment with ACE-inhibitors is associated with less severe disease with SARS-Covid-19 infection in a multi-site UK acute Hospital Trust](https://www.researchgate.net/publication/340261837_Treatment_with_ACE-inhibitors_is_associated_with_less_severe_disease_with_SARS-Covid-19_infection_in_a_multi-site_UK_acute_Hospital_Trust?channel=doi&linkId=5e806057a6fdcc139c10467a&showFulltext=true)

work in progress

```
annr = DrugMentionNLP.DrugAnnotator(["drug1", "drug2"])
result = annr.annotate("my document text with drug 1")
```

.annotate returns each mention of each drug tagged for negation and with the surrounding context

## Usage
DrugMentionNLP.py contains the OACAnnotator class which does all the work, the only method used externally is .annotate()

Demo usage in demo.py which also uses utils.py to format the output of the annotator to a convenient pandas dataframe. The demo script also demonstrates using a csv of drug brand/generic names to easily filter and group drugs for analysis.  

Currently basic negation and allergy detection is enabled by default. 

## Funding
Dan Bean is funded by Health Data Research UK

## Contact
Developed by Dan Bean at King's College London - daniel.bean@kcl.ac.uk
