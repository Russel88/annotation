# Prokaryotic Genome Annotation pipeline

## Install

miniconda or anaconda is needed

### Make conda envs
`conda env create --name annotation -f=environment.yml`

`conda env create --name antismash -f=environment_antismash.yml`

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

### CasFinder
Download HMMs from:
https://crisprcas.i2bc.paris-saclay.fr/Home/DownloadFile?filename=CRISPRCasFinder.zip

`hmmpress CRISPRCasFinder/CasFinder-2.0.2/CASprofiles-2.0.2/*.hmm`

### GNU parallel
Install GNU parallel if not already installed

`conda activate annotation`

`conda install -c conda-forge parallel` 

## How to run

**Edit the config.yml file to point to the software and databases**

`conda activate annotation`

`./annotate -h`


