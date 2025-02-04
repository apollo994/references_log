# genomes_log
A set of scripts to automate the dowload and tracking of assembles and annotations in a shared file system

### organize_ncbi.py
This script takes a unzipped ncbi datasets folder and a target location. The ncbi folder is copied into the target folder following the `species/assembly/file` structure. Additionally metadata are saved. Currently the scripts only works with *fna and *gff3 files.

An example ncbi comand to get all SAR assemblies is:
```
# dowload the dataset
datasets download genome taxon 2698737 --assembly-level chromosome,complete --annotated --reference  --include genome,gff3
# unzip archive
unzip ncbi_dataset.zip
# organize the assemblies in the target folder 
python organize_ncbi.py --ncbi ncbi_dataset --target target_folder

``` 
