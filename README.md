# MetaSRA

This pipeline will fetch metadata from the Sequence Read Archive(SRA) givin a list of Study Accession IDs and outputs it in a csv file(s). This output is for each Run Accession ID
in the study and includes:
* Study Title
* Abstract
* LIBRARY_CONSTRUCTION_PROTOCOL
* Sample Description(Cell-Tissue Type)
* Study Design

In addition to fetching the metadata, it filters out single-end reads and takes the paired-end reads and sperates them ou into (Single-Cell, Bulk, and BCR) RNA-Seq. 

##Prerequisites
```
conda create -n MetaSRA python=3.7
conda activate MetaSRA
conda install -c bioconda entrez-direct 
```

##Getting started
To get started place your Study Accession IDs "SRP294125" in a file called "SRPids".
Then to run MetaSRA use this command:
```
python MetaSRA 
```

The output will be at most 4 files:
* metadata_single_cell
* metadata_bulk
* metadata_BCR
* single_end

conda env create -f environment.yaml

conda activate MetaSRA
