# MetaSRA

Givin a list of Study Accession IDs(SRP294125) or (BioProject IDs(PRJNA163279) or GEO acc. #'s(GSM927308)) , this pipeline will fetch metadata from the Sequence Read Archive(SRA) and output it in a csv format. Output includes:
* Study Title
* Abstract
* Sample Description(Cell-Tissue Type)
* Patient data (Age, Sex, Race, disease state, ect) 


Single-end and paired-end reads are marked and sperated  into (Single-Cell, Bulk, and BCR) RNA-Seq. 

##Prerequisites
```
conda env create -f environment.yaml
conda activate MetaSRA
```

##Getting started
To get started place your Study Accession IDs in a file called "SAids".
Then to run MetaSRA use this command:
```
python MetaSRA 
```

The output will be at most 3 files:
* metadata_single_cell
* metadata_bulk
* metadata_BCR



