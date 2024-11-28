import sys
import os
import subprocess
import pandas as pd

def check_entry(entry, column, tsv):

    df = pd.read_csv(tsv, sep='\t', header=0)
    
    # Check if an entry is already present in a column
    if entry in df[column].values:
        print(f"{entry} already exists in the {column} field of {tsv}")
        sys.exit()
    
def make_folder(sp, base_dir):
    
    # Create a folder named after the species in the specified directory
    folder_path = os.path.join(base_dir, sp)
    os.makedirs(folder_path, exist_ok=True)
    absolute_path = os.path.abspath(folder_path)

    return absolute_path


def download_file(url, folder):
    
    # Use wget to download the file
    try:
        command = ["wget", "-P", folder, url]
        subprocess.run(command, check=True)

        # Extract the filename from the URL
        file_name = os.path.basename(url)
        file_path = os.path.join(folder, file_name)

        # Return the absolute path of the downloaded file
        print (f"File saved at {file_path}")
        return os.path.abspath(file_path)

    except subprocess.CalledProcessError as e:
        os.rmdir(folder) # remove folder if error is raised
        print (f"Error downloading file: {e.stderr.decode()}")
        sys.exit()

def add_entry(sp, tax, url, tsv):

    df = pd.read_csv(tsv, sep='\t', header=0)
    
    # Add new entry to the TSV
    new_row = {'species': sp, 'taxid': tax, 'url': url}
    new_row_df = pd.DataFrame([new_row])
    updated_df = pd.concat([df, new_row_df], ignore_index=True)

    # Save the updated DataFrame back to the TSV
    updated_df.to_csv(tsv, sep='\t', index=False)
    print(f"Added new entry to {tsv}: {new_row}")


def main():

    if len(sys.argv) != 4:
        print("Usage: python script.py <species_name> <taxon_id> <url>")
        sys.exit(1)

    sp = sys.argv[1]
    tax = sys.argv[2]
    url = sys.argv[3]

    # Check if entry is present in log
    check_entry(sp, 'species', 'genomes.tsv')
    check_entry(tax, 'taxid', 'genomes.tsv')
    check_entry(url, 'url', 'genomes.tsv')

    # Create folder
    folder_path = make_folder(sp, '../genomes')
    
    # Download file
    file_path = download_file(url, folder_path)

    # Add entry
    add_entry(sp, tax, url , 'genomes.tsv')

if __name__ == "__main__":
    main()