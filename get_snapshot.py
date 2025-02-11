import os
import sys
import datetime

def get_folder_size(path):
    """
    Calculates the total size of a folder by summing up all file sizes.

    :param path: Folder path
    :return: Total size in bytes
    """
    total_size = 0
    for dirpath, _, filenames in os.walk(path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if os.path.isfile(filepath):
                total_size += os.path.getsize(filepath)
    return total_size

def generate_snapshot(folder_path):
    """
    Generates a snapshot of the folder structure up to the second level.
    Saves the output in a timestamped text file inside the 'snapshot' folder.

    :param folder_path: Path to the folder to scan.
    """
    # Create the snapshot directory if it doesn't exist
    snapshot_dir = "snapshot"
    os.makedirs(snapshot_dir, exist_ok=True)

    # Generate timestamped filename
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_file = os.path.join(snapshot_dir, f"snapshot_{timestamp}.txt")

    # Count number of species (first-level directories)
    species_count = sum(1 for item in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, item)))

    # Get total folder size
    total_size_bytes = get_folder_size(folder_path)
    total_size_mb = total_size_bytes / (1024 * 1024)  # Convert to MB

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"Snapshot of: {folder_path}\n")
        f.write("=" * 50 + "\n")
        f.write(f"Number of species (first-level folders): {species_count}\n")
        f.write(f"Total size of the folder: {total_size_mb:.2f} MB ({total_size_bytes} bytes)\n")
        f.write("=" * 50 + "\n")

        for root, dirs, files in os.walk(folder_path):
            # Get relative depth
            depth = root[len(folder_path):].count(os.sep)
            
            # Stop scanning deeper than the second level
            if depth > 1:
                continue
            
            indent = "    " * depth
            f.write(f"{indent}{os.path.basename(root)}/\n")
            
            # Write files with extra indentation
            for file in files:
                f.write(f"{indent}    {file}\n")

    print(f"Snapshot saved to {output_file}")

if __name__ == "__main__":
    # Ensure a folder path is provided
    if len(sys.argv) != 2:
        print("Usage: python folder_snapshot.py <folder_path>")
        sys.exit(1)

    folder_path = sys.argv[1]

    if os.path.isdir(folder_path):
        generate_snapshot(folder_path)
    else:
        print("Error: Invalid folder path.")
