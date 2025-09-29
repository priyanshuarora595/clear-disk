import math
import os
import shutil
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

# Lock for thread-safe print
print_lock = threading.Lock()


def get_free_space(path="/"):
    """Get free disk space in bytes."""
    stat = shutil.disk_usage(path)
    return stat.free


def copy_file(file_path, target_file, i, total):
    """Threaded file copy."""
    shutil.copyfile(file_path, target_file)
    with print_lock:
        print(f"Copied file {i+1}/{total} to {target_file}")


def fill_disk_with_file(file_path, target_dir, buffer_size_gb=0, max_workers=8):
    """Fill the disk with copies of the specified file, leaving a buffer, using multithreading."""
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    file_size = os.path.getsize(file_path)
    free_space = get_free_space(target_dir)
    buffer_size = buffer_size_gb * 1024**3  # Convert GB to bytes

    ext = file_path.split(".")[-1]
    usable_space = free_space - buffer_size

    if usable_space <= 0:
        raise ValueError("Not enough free space available after buffer.")

    num_copies = math.floor(usable_space / file_size)

    print(f"Free space: {free_space / 1024 ** 3:.2f} GB")
    print(f"Usable space after buffer: {usable_space / 1024 ** 3:.2f} GB")
    print(f"File size: {file_size / 1024 ** 2:.2f} MB")
    print(f"Number of copies to create: {num_copies}")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for i in range(num_copies):
            target_file = os.path.join(target_dir, f"copy_{i}.{ext}")
            futures.append(
                executor.submit(copy_file, file_path, target_file, i, num_copies)
            )

        # Optional: wait for all to complete and catch any exception
        for future in as_completed(futures):
            future.result()  # Re-raises exceptions if any

    print("Disk filling completed successfully!")


if __name__ == "__main__":
    file_to_copy = input("Enter path of the file to copy: ")
    destination_dir = input("Enter the path to dump all files: ")

    try:
        fill_disk_with_file(
            file_to_copy, destination_dir, buffer_size_gb=0.3, max_workers=16
        )
    except Exception as e:
        print(f"Error: {e}")
