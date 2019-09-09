# Prokaryotic Genome Annotation pipeline

This is a pipeline to run multiple annnotation tools, and compile the output in some nice comparable and easily usable tables.
The pipeline is written to work optimally or our own server, and might be challenging to implement other places. 
However, below are the different steps which should be enough to get things working.

Caution: The script is not written in a "safe" way, that is, if something fails, so might the rest of the script, and useful error messages are not necessarily produced.

## Citation
[![DOI](https://zenodo.org/badge/184105796.svg)](https://zenodo.org/badge/latestdoi/184105796)

## Installation

miniconda or anaconda is needed

### Clone
`git clone https://github.com/Russel88/annotation.git`

`cd annotation`

### Make conda environment
`conda env create -n annotation -f=environment.yml`

### Install KOfam_scan and download database
See instructions here: ftp://ftp.genome.jp/pub/tools/kofamscan/

`wget ftp://ftp.genome.jp/pub/db/kofam/profiles.tar.gz`

### Install eggNOG-mapper and download eggNOG bact diamond database
See instructions here: https://github.com/eggnogdb/eggnog-mapper

### Install dbCAN2 and download associated CAZyme databases
`git clone https://github.com/Russel88/run_dbcan.git`

Download databases as described here https://github.com/linnabrown/run_dbcan

### Install SignalP
See instructions here: http://www.cbs.dtu.dk/services/SignalP/

## Download and prepare databases
### MEROPS
`wget ftp://ftp.ebi.ac.uk/pub/databases/merops/current_release/pepunit.lib`

`awk '{print $1}' pepunit.lib > pepunit.faa`

`diamond makedb --in pepunit.faa -d merops`

### TnpPred
Get HMMs:

`wget https://www.mobilomics.cl/tnppred/downloads/TnpPred_HMM_Profiles.hmm`

`hmmpress TnpPred_HMM_Profiles.hmm`

### RGI
Download database: https://github.com/arpcard/rgi

## How to run

**Edit the config.yml file to point to the software and databases**

`conda activate annotation`

`./annotate -h`


