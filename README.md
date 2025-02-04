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
python organize_ncbi.py --ncbi ncbi_dataset --target target_folder/

``` 
### get_snapshot.py
This script takes a folder with the structure of `species/assemblies/file` and it produces a snapshot to use in case someone wants to recreate the same folder structure. The snapshot is saved in the `snapshot/` foder and can be tracked using `git`. 
```
python get_snapshot.py target_folder
``` 
