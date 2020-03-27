# DrugPipeline

Modified from https://github.com/CogStack/OAC-NLP

work in progress

```
annr = DrugMentionNLP.DrugAnnotator(["drug1", "drug2"])
result = annr.annotate("my document text with drug 1")
```

.annotate returns each mention of each drug tagged for negation and with the surrounding context

## Overview

Most of the regular expressions are used to detect negations, or any other keyword that means the drug is not currently being taken. Cases considered are:

* Stopping, withholding, discontinuing
* Allergy
* Medication switching (A switched to B -> A is negated)
* Consider / consider restarting (e.g. after surgery)

## Usage
DrugMentionNLP.py contains the OACAnnotator class which does all the work, the only method used externally is .annotate()

## Funding
Dan Bean is funded by Health Data Research UK

## Contact
Developed by Dan Bean at King's College London - daniel.bean@kcl.ac.uk