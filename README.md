# Pubmed_COVID19_Pathways
API Tool to collect gene expression pathways from Pubmed for new COVID19 research .

## Author
Clark Xu - June 16, 2020

## Purpose
The script makes API Calls to Pubmed to collect gene expression of pathways linked to coronavirus. It outputs gene expression in CSV File Format to facilitate drug ranking in targeted pharmaceutical research. Contribution to the PAGER-COV Project.

Pubmed API  documented at: https://pubchemdocs.ncbi.nlm.nih.gov/programmatic-access <br>
PAGER-COV documented at: http://discovery.informatics.uab.edu/PAGERCOV/

## Specifications and Dependencies
### Specifications:
Python 3
### Dependencies:
urllib, pandas, os, tdqm, ratelimit

## Details
Pubmed features transformed into CSV: <br>
pathwayname, genelist, genecount

Script Name: <br>
Pubchem_COVID_Pathways.py

Script Input (Optional if using preloaded COVID pathways): <br>
PubChem_pathway_text_COVID-19.csv

Script Output: <br>
rPubmed_pathway_gene_expression_COVID-19.csv

The script takes about 20 - 30 minutes to run. The estimated number of COVID pathways are about 1,500.

## Licensing (The MIT License)
Copyright 2020 Clark Xu

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
