import os
import subprocess
import pytsk3  # Library used to read NTFS file metadata
import ntpath  # For path manipulation

# Define your source and destination paths
dsk_src = "/dev/sdX"   # Source disk
mnt_src = "/mnt/XXXX"  # Mount point of disk (usually root - /
dsk_dst = "/dev/sda4"  # Destination disk 
directory = "home/username/directory/directory" # Do not repeat mnt_src again

# Function to read crtime from NTFS using pytsk3
def get_crtime_ntfs(filepath):
    img = pytsk3.Img_Info(dsk_src)
    fs = pytsk3.FS_Info(img)
    ntfs_file = fs.open(filepath)

    for attr in ntfs_file:
        if attr.info.type == pytsk3.TSK_FS_ATTR_TYPE_NTFS_FNAME:
            crtime = attr.info.crtime
            return crtime
    
    return None

# Function to set crtime using debugfs
def set_crtime_ext4(filepath, dsk_dst, crtime):
    crtime_hex = hex(int(crtime))
    crtime_lo = crtime_hex[-8:]
    crtime_hi = crtime_hex[:-8] if len(crtime_hex) > 8 else "0"

    set_crtime_lo_cmd = f"debugfs -w {dsk_dst} -R 'set_inode_field \"{filepath}\" crtime_lo 0x{crtime_lo}'"
    set_crtime_hi_cmd = f"debugfs -w {dsk_dst} -R 'set_inode_field \"{filepath}\" crtime_hi 0x{crtime_hi}'"

    subprocess.run(set_crtime_lo_cmd, shell=True, check=True)
    subprocess.run(set_crtime_hi_cmd, shell=True, check=True)

# Main script
try:
    os.chdir(mnt_src)
except FileNotFoundError:
    print(f"Error: Directory {mnt_src} not found.")
    exit(1)

for root, dirs, files in os.walk(directory):
    for name in files:
        filepath = os.path.join(root, name)
        rel_filepath = os.path.relpath(filepath, mnt_src)

        # Get crtime from NTFS source
        crtime = get_crtime_ntfs(ntpath.join("/", rel_filepath))
        if crtime is None:
            print(f"Skipping {rel_filepath}: crtime not found.")
            continue

        # Set crtime on ext4 destination
        set_crtime_ext4(rel_filepath, dsk_dst, crtime)
        print(f"Set crtime for {rel_filepath}")

print("Done.")
