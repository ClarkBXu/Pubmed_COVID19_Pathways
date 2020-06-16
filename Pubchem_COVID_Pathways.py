# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 10:16:53 2020

@author: CBX033
"""

import urllib.request as req
import pandas as pd 
import os
from tqdm import tqdm
from ratelimit import limits

#From Pubchem: No more than 400 requests per minute
ONE_MINUTE = 60
@limits(calls=400,period=ONE_MINUTE)

def percentEncoding(query,reservedCharactersDict):
    """
    Input: query - str with raw command, 
           reservedCharactersDict - dict with reserved characters for percent encoding
                                    Key is reserved character
                                    Value is encoding for reserved character
    Output: encodedQuery - str with percent encoding and query wrapper
    """
    #Add Query Wrapper
    urlQuery = "query={ " + query + " }"
    #Perform Percent Encoding
    tempQuery = urlQuery
    for entry in reservedCharactersDict:
        encodedQuery = tempQuery.replace(entry,reservedCharactersDict.get(entry))
        tempQuery = encodedQuery
    return encodedQuery

def sourceLocation(local,fileName="PubChem_pathway_text_COVID-19.csv"):
    """
    Input: local - bool 
                   True if file in directory
                   False otherwise,
           filename - str of file name of CSV for Pubchem coronavirus pathways
    Output: read - pandas dataframe object representing Pubchem pathways for coronavirus
    """
    #Read from Directory if File is Local
    if local:
        read = pd.read_csv(fileName)
    #Read from Pubchem Website if File is Not Local
    else:
        urlHome = "https://pubchem.ncbi.nlm.nih.gov"
        urlExtension = "/sdq/cgi2rcgi.cgi"
        urlInput = "infmt=json"
        urlOutput = "outfmt=csv"
        urlQuery = percentEncoding(query = "download : * , "
                                           "collection : pathway , "
                                           "where :{ ands :[{ * : COVID-19 }]}, "
                                           "order :[ relevancescore,desc ], "
                                           "start :1, "
                                           "limit :10000000, "
                                           "downloadfilename : PubChem_pathway_text_COVID-19",
                                   reservedCharactersDict = {' ':'%22',})
        #Construct URL
        response = req.urlopen(urlHome + urlExtension + '?' + urlInput + '&' + urlOutput + '&' + urlQuery)
        #Check for OK Status - HTTP 200
        if response.getcode() != 200:
            raise Exception('API Response: Status Code {}'.format(response.getcode()))
        #Read CSV
        read = pd.read_csv(response)
    return read

def getPathwayMetadata(source):
    """
    Input: source - pandas dataframe object with Pathway ID
    Output: metadata - pandas dataframe object with Pathway Name, Gene List, Gene Count
    """
    #Initialize metadata
    metadata = pd.DataFrame(columns=[])
    #Initialize new metadata columns
    pathDesc = []
    geneList = []
    geneCount = []
    #Initialize gene list url
    urlHome = "https://pubchem.ncbi.nlm.nih.gov"
    urlExtension = "/assay/pcget.cgi"
    urlTask = ("task=pathway_gene&"
               "pathwayid=***&"
               "start=1&"
               "limit=10000000&"
               "download=true&"
               "downloadfilename=PathwayID_***_pcget_pathway_gene")
    #Get metadata
    for i in tqdm(source.index): 
        tempList = []
        try:
            #Access Gene List via URL using Pathway ID
            newURL = urlTask.replace('***',str(source['pathwayid'][i]))
            response = req.urlopen(urlHome + urlExtension + '?' + newURL)
            read = pd.read_csv(response)
            #Get all Gene Symbols in Gene List
            j = 0
            for entry in read['genesymbol']:
                tempList.append(entry)
                j += 1
            #Add Pathway Description, Gene List and Gene Count to metadata columns
            pathDesc.append(str(source['name'][i]))
            geneList.append(tempList)
            geneCount.append(j)
        except:
            print("\nError at Pathway ID in row",i)
    #Add metadata columns  
    metadata['pathwayname'] = pathDesc
    metadata['genelist'] = geneList
    metadata['genecount'] = geneCount    
    return metadata

def main():
    #Load Source
    ##If data is in directory:
    #data = sourceLocation(local=True)
    ##By default, search in Pubchem:
    data = sourceLocation(local=False,fileName='')
    if not data.empty:
        print('Source loading complete')
    
    #Load Metadata
    result = getPathwayMetadata(source=data)
    if not result.empty:
        print('Metadata loading complete')
    
    #Create CSV
    fileName = 'rPubmed_pathway_gene_expression_COVID-19.csv'
    result.to_csv(fileName,index=False)
    files = os.listdir()
    if fileName in files:
        print("Script Done")

if __name__ == '__main__':
    main()