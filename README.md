# genomes_log
A set of scripts to automate the dowload and tracking of assembles and annotations in a shared file system

### organize_ncbi.py
This script takes a unzipped ncbi datasets folder and a target location. The ncbi folder is copied into the target folder following the `target_folder/species/assembly/file` structure. Additionally metadata are saved. Currently the scripts only works with *fna and *gff3 files.

#### Dependencies 
- [NCBI dataset API](https://www.ncbi.nlm.nih.gov/datasets/docs/v2/command-line-tools/download-and-install/)
- python and pandas

An example ncbi comand to get all SAR assemblies is:
```
# dowload a dataset of multiple species 
datasets download genome taxon 2698737 --assembly-level chromosome,complete --annotated --reference  --include genome,gff3
# or download a single assembly
datasets download genome accession GCF_028858775.2 --include gff3,genome
# unzip archive
unzip ncbi_dataset.zip
# organize the assemblies in the target folder (this is the folder where the species folder will be created)
python organize_ncbi.py --ncbi ncbi_dataset --target target_folder/

``` 
### get_snapshot.py
This script takes a folder with the structure of `species/assemblies/file` and it produces a snapshot to use in case someone wants to recreate the same folder structure. The snapshot is saved in the `snapshot/` foder and can be tracked using `git`. 
```
python get_snapshot.py target_folder
``` 
