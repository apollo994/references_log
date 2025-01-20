# This script takes a unzipped ncbi datasets folder and a taget location
# The ncbi folder is copied into the target folder following the 
# species/assembly/file structure. Additionally metadata are saved.
# Currently the scripts only works with *fna and *gff3 files.
# An example ncbi comand to get the data is:
# datasets download genome taxon 2698737 --assembly-level chromosome,complete --annotated --reference  --include genome,gff3
# the command above downloads all SAR genomes and annotations
# with the specified carachteristics 

import pandas as pd
import json
import argparse
import os
import shutil
from glob import glob

def unpack_nested_columns(dataframe, column_name):
    """Unpack a nested JSON column in a DataFrame."""
    unpacked_df = pd.json_normalize(dataframe[column_name].dropna())
    unpacked_df.columns = [f"{column_name}.{sub_col}" for sub_col in unpacked_df.columns]
    return dataframe.drop(column_name, axis=1).join(unpacked_df)


def main():

    # parse input
    parser = argparse.ArgumentParser(description='Sort ncbi datatset folder')
    parser.add_argument('--ncbi', help='Unzipped ncbi folder (generally called ncbi_dataset)')
    parser.add_argument('--target',help='The folder to populate with species folder')
    args = parser.parse_args()


    # Read assembly data
    assembly_data_report = f"{args.ncbi}/data/assembly_data_report.jsonl"
    df = pd.read_json(assembly_data_report, lines=True)

    # Identify nested columns
    nested_columns = [col for col in df.columns if df[col].apply(lambda x: isinstance(x, dict)).any()]

    # Iteratively unpack all nested columns
    for column in nested_columns:
        df = unpack_nested_columns(df, column)
    
    # cycle over each assembly in the ncbi_dataset folder
    for assembly_name in df.accession.values:
        tmp_df = df[df.accession == assembly_name]
        species_name = (tmp_df["organism.organismName"].map(lambda x: x.replace('.', '_')
                                                         .replace(' ', '_')
                                                         .replace('__', '_')
                                                         .replace('/', '_'))
                        + '.'
                        + tmp_df["organism.taxId"].astype(str)).values[0]
    
        # Get the filename without extension
        fna_files = glob(f'{args.ncbi}/data/{assembly_name}/*.fna')
        if not fna_files:
            raise FileNotFoundError(f"No .fna file found in {source_copy}/{assembly_name}")
        filename = os.path.splitext(os.path.basename(fna_files[0]))[0]
    
        # Define source and target paths
        source_genome = f'{args.ncbi}/data/{assembly_name}/*.fna'
        source_ann = f'{args.ncbi}/data/{assembly_name}/*.gff'
        target_folder_path = os.path.join(args.target, species_name, assembly_name)
        target_genome = os.path.join(target_folder_path, f'{filename}.fna')
        target_ann = os.path.join(target_folder_path, f'{filename}.gff')
    
        # Create the target directory if it doesn't exist
        os.makedirs(target_folder_path, exist_ok=True)
    
        # Copy genome and annotation files
        for source_file in glob(source_genome):
            shutil.copy(source_file, target_genome)
        for source_file in glob(source_ann):
            shutil.copy(source_file, target_ann)
        
        # transpose and save assembly metadata
        tmp_df = tmp_df.transpose()
        info_file = f'{args.target}/{species_name}/{assembly_name}/{assembly_name}.info.csv'
        tmp_df.to_csv(info_file, header = False)

        print(species_name, 'genome, annotation and metadata copied!')

if __name__ == "__main__":
    main()

