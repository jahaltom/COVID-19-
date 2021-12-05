# MetaSRA

Given a list of Study Accession IDs (SRP294125), BioProject IDs (PRJNA163279), or GEO_Accession IDs (GSM927308), this pipeline will fetch metadata from the Sequence Read Archive(SRA) for each run and output it in a csv format. Output includes:
* Study Title
* Abstract
* Sample Description(Cell-Tissue Type)
* Patient data (Age, Sex, Race, disease state, ect) 
* library_layout (Single-end or Paired-end)

Output is sperated into Single-Cell, Bulk, and BCR RNA-Seq.

**Prerequisites**
```
conda env create -f environment.yaml
conda activate GetMetaSRA
```

**Getting started**

To get started place your Study Accession IDs in a file called "SAids".
Then to run MetaSRA use this command:
```
python GetMetaSRA.py 
```

The output will be at most 3 files:
* metadata_single_cell
* metadata_bulk
* metadata_BCR



