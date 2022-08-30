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

# Parallelize
```
split -l 25 SAids

ls *xa* | cat > splits

cat splits | while read i; do
	mkdir Dir$i
	cat $i > Dir$i/SAids
	cp GetMetaSRA.py Dir$i/
	cp script Dir$i/
	sbatch Dir$i/script
done
```




#Script
```
#!/bin/bash

#SBATCH --time=24:00:00   # walltime limit (HH:MM:SS)
#SBATCH --nodes=1   # number of nodes
#SBATCH --ntasks-per-node=50   # 30 processor core(s) per node
#SBATCH -p RM-shared


source activate GetMetaSRA
python GetMetaSRA.py 
```

