import sys
import os
import csv
import subprocess

def check_entry(entry, column, tsv):
    """
    Check if an entry already exists in a specified column of a TSV file.
    """
    if not os.path.exists(tsv):
        return  # If the file doesn't exist, nothing to check

    with open(tsv, mode='r', newline='') as file:
        reader = csv.DictReader(file, delimiter='\t')
        for row in reader:
            if row[column] == entry:
                print(f"{entry} already exists in the {column} field of {tsv}")
                sys.exit()

def make_folder(sp, base_dir):
    """
    Create a folder named after the species in the specified directory.
    """
    folder_path = os.path.join(base_dir, sp)
    os.makedirs(folder_path, exist_ok=True)
    return os.path.abspath(folder_path)

def download_file(url, folder):
    """
    Download a file from a given URL into a specified folder using wget.
    """
    try:
        command = ["wget", "-P", folder, url]
        subprocess.run(command, check=True)

        file_name = os.path.basename(url)
        file_path = os.path.join(folder, file_name)

        print(f"File saved at {file_path}")
        return os.path.abspath(file_path)

    except subprocess.CalledProcessError as e:
        os.rmdir(folder)  # Remove folder if error is raised
        print(f"Error downloading file: {e}")
        sys.exit()

def add_entry(sp, tax, url, tsv):
    """
    Add a new entry to the TSV file.
    """
    new_row = {'species': sp, 'taxid': tax, 'url': url}
    file_exists = os.path.exists(tsv)

    with open(tsv, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['species', 'taxid', 'url'], delimiter='\t')

        # Write header if the file is being created
        if not file_exists:
            writer.writeheader()

        # Add the new row
        writer.writerow(new_row)
        print(f"Added new entry to {tsv}: {new_row}")

def main():
    if len(sys.argv) != 4:
        print("Usage: python script.py <species_name> <taxon_id> <url>")
        sys.exit(1)

    sp = sys.argv[1]
    tax = sys.argv[2]
    url = sys.argv[3]

    tsv = 'genomes.tsv'

    # Check if the entry is already present in the log
    check_entry(sp, 'species', tsv)
    check_entry(tax, 'taxid', tsv)
    check_entry(url, 'url', tsv)

    # Create a folder for the species
    folder_path = make_folder(sp, '../genomes')

    # Download the file
    download_file(url, folder_path)

    # Add the entry to the TSV file
    add_entry(sp, tax, url, tsv)

if __name__ == "__main__":
    main()
