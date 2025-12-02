import os
from PIL import Image

# --- Configuration ---
# The script scans all subdirectories from the ROOT_DIR_TO_SCAN.
FOLDER_TO_SEARCH = "breathing"
INPUT_SEARCH_PATTERN = "breathing_000.png"
OUTPUT_FILENAME_PATTERN = "thumbnail_16x16.png"
ROOT_DIR_TO_SCAN = "." # Start scan from the current directory

TARGET_SIZE = (16, 16) # The desired final size

def process_single_image(input_path, output_path, size):
    """
    Loads an image and simply downsamples it to the target size.
    
    :param input_path: Full path to the input image.
    :param output_path: Full path to save the output image.
    :param size: The target dimensions (16x16).
    """
    try:
        # 1. Open the image (keeping its original mode, including transparency if present)
        img = Image.open(input_path)

        # 2. Downsample the image to 16x16 using LANCZOS for high-quality subsampling.
        resized_img = img.resize(size, Image.Resampling.LANCZOS)

        # 3. Save the processed image.
        resized_img.save(output_path)
        print(f"   -> SUCCESS: Thumbnail saved at {output_path}")

    except Exception as e:
        # Using a more informative error message that includes the failing file path
        print(f"   -> ERROR processing {input_path}: {e}")

def create_thumbnails_batch(root_dir):
    """
    Walks through the file system to find and process all 'breathing/breathing_000.png' images.
    """
    print(f"--- Starting thumbnail batch processing from root directory: {os.path.abspath(root_dir)} ---")
    processed_count = 0
    
    # os.walk traverses the directory tree
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Check if the current directory is named 'breathing' AND contains the input file
        if os.path.basename(dirpath) == FOLDER_TO_SEARCH and INPUT_SEARCH_PATTERN in filenames:
            
            input_file_path = os.path.join(dirpath, INPUT_SEARCH_PATTERN)
            
            # Get the parent directory (one level up from 'breathing')
            parent_dir = os.path.dirname(dirpath)
            
            # Construct the output path in the parent directory
            output_file_path = os.path.join(parent_dir, OUTPUT_FILENAME_PATTERN)
            
            print(f"Processing found input: {input_file_path}")
            print(f"   Saving output to parent folder: {output_file_path}")
            
            # Use the single image processing function
            process_single_image(input_file_path, output_file_path, TARGET_SIZE)
            processed_count += 1
    
    print(f"\n--- Batch processing complete. {processed_count} images processed. ---")

if __name__ == "__main__":
    # Ensure Pillow is installed: pip install Pillow
    create_thumbnails_batch(ROOT_DIR_TO_SCAN)