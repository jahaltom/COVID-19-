# MetaSRA

This pipeline will fetch metadata from the Sequence Read Archive(SRA) givin a list of Study Accession IDs and outputs it in a csv file(s). Output includes:
* Study Title
* Abstract
* Sample Description(Cell-Tissue Type)
* Patient data (Age, Sex, Race, disease state, ect) 


In addition to fetching the metadata, it filters out single-end reads and takes the paired-end reads and sperates them ou into (Single-Cell, Bulk, and BCR) RNA-Seq. 

##Prerequisites
```
conda env create -f environment.yaml
conda activate MetaSRA
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


