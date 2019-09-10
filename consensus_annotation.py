#!/usr/bin/env python2
import pandas as pd
import numpy as np
import sys

# Read data
dat = pd.read_csv(sys.argv[1], sep ='\t', skiprows = 2)

tools = list(sys.argv[3].split(","))

# Define functions partioning data.frame in known and unknown fraction for each tool
def prokka(dd):
    return [dd[dd['Annotation_prokka'] != "hypothetical protein"][['#CDS','Contig_Start_End_Strand','Annotation_prokka']],
            dd[dd['Annotation_prokka'] == "hypothetical protein"]]
def kofamName(dd):
    dd1 = dd[dd['Annotation_KOfam'].notna()]
    return [dd1[~dd1['Annotation_KOfam'].str.contains("uncharacterized")][['#CDS','Contig_Start_End_Strand','Annotation_KOfam']],
           dd[dd['Annotation_KOfam'].isna() | dd['Annotation_KOfam'].str.contains("uncharacterized")]]
def kofamKO(dd):
    return [dd[dd['KO_KOfam'].notna()][['#CDS','Contig_Start_End_Strand','KO_KOfam']],
            dd[dd['KO_KOfam'].isna()]]
def dbcan(dd):
    return [dd[dd['CAZy'].notna()][['#CDS','Contig_Start_End_Strand','CAZy']],
           dd[dd['CAZy'].isna()]]
def eggnogName(dd):
    return [dd[dd['Annotation_eggNOG'].notna()][['#CDS','Contig_Start_End_Strand','Annotation_eggNOG']],
            dd[dd['Annotation_eggNOG'].isna()]]
def eggnogKO(dd):
    return [dd[dd['KO_eggNOG'].notna()][['#CDS','Contig_Start_End_Strand','KO_eggNOG']],
            dd[dd['KO_eggNOG'].isna()]]
def merops(dd):
    return [dd[dd['MEROPS'].notna()][['#CDS','Contig_Start_End_Strand','MEROPS']],
           dd[dd['MEROPS'].isna()]]
def rgi(dd):
    return [dd[dd['RGI'].notna()][['#CDS','Contig_Start_End_Strand','RGI']],
            dd[dd['RGI'].isna()]]
def tnppred(dd):
    return [dd[dd['TnpPred'].notna()][['#CDS','Contig_Start_End_Strand','TnpPred']],
            dd[dd['TnpPred'].isna()]]

# Switcher function to run sub-functions
def consensus(tool, ddd):
    switcher = {
        'prokka': lambda: prokka(ddd),
        'kofamName': lambda: kofamName(ddd),
        'kofamKO': lambda: kofamKO(ddd),
        'dbcan': lambda: dbcan(ddd),
        'eggnogName': lambda: eggnogName(ddd),
	'eggnogKO': lambda: eggnogKO(ddd),
        'merops': lambda: merops(ddd),
        'rgi': lambda: rgi(ddd),
        'tnppred': lambda: tnppred(ddd)
    }
    fun = switcher.get(tool, lambda: "Invalid name")
    return fun()

# Check if tools have been run
tools_included = []
cols = dat.columns
for i in tools:
    if i == 'prokka':
        if 'Annotation_prokka' in cols:
            tools_included.append(i)
    if i == 'kofamName':
        if 'Annotation_KOfam' in cols:
            tools_included.append(i)
    if i == 'kofamKO':
        if 'KO_KOfam' in cols:
            tools_included.append(i)
    if i == 'dbcan':
        if 'CAZy' in cols:
            tools_included.append(i)
    if i == 'eggnogName':
        if 'Annotation_eggNOG' in cols:
            tools_included.append(i)
    if i == 'eggnogKO':
        if 'KO_eggNOG' in cols:
            tools_included.append(i)
    if i == 'merops':
        if 'MEROPS' in cols:
            tools_included.append(i)
    if i == 'rgi':
        if 'RGI' in cols:
            tools_included.append(i)
    if i == 'tnppred':
        if 'TnpPred' in cols:
            tools_included.append(i)

# Nested loop of the annotations
print "Getting consensus annotation with the following hierarchy:\n" + str(tools_included).replace(","," >")

unknown = dat
knowns = []
for i in tools_included:
    sub = consensus(i, unknown)
    unknown = sub[1]
    knowns.append(sub[0])

# Combine annotate in one data.frame
df = pd.DataFrame(np.concatenate(knowns, axis=0), columns=['#CDS','Contig_Start_End_Strand','Annotation'])

print str(len(df)) + " out of " + str(len(dat)) + " CDSs annotated"

# Add unknowns
df_uk = dat[dat['#CDS'].isin(set(df['#CDS']).symmetric_difference(set(dat['#CDS'])))][['#CDS','Contig_Start_End_Strand','Annotation_prokka']]
df_uk.columns = ['#CDS', 'Contig_Start_End_Strand', 'Annotation']
df_uk['Annotation'] = "NA"

df = df.append(df_uk).sort_values('#CDS')

# Add columns if possible
if 'CGC' in cols:
    df = df.merge(dat[['#CDS','CGC']])

if 'antiSMASH' in cols:
    df = df.merge(dat[['#CDS','antiSMASH']])

if 'SignalP' in cols:
    df = df.merge(dat[['#CDS','SignalP']])

# Write to file
df.to_csv(sys.argv[2], sep='\t', index=False, na_rep="NA")
