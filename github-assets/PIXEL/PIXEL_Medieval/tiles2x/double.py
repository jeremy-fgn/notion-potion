import os
from PIL import Image

# --- Configuration ---
ROOT_DIR_TO_SCAN = "." # Start scan from the current directory
TARGET_SCALE_FACTOR = 2 # 4x scale factor (8x8 -> 32x32)
SOURCE_TILE_SIZE = (8, 8) # Assuming all original tiles are 8x8
TARGET_TILE_SIZE = (SOURCE_TILE_SIZE[0] * TARGET_SCALE_FACTOR, 
                    SOURCE_TILE_SIZE[1] * TARGET_SCALE_FACTOR) # Will be 32x32

def upscale_image(input_path, output_path, target_size):
    """
    Loads an image and upscales it to the target size using Nearest Neighbor 
    to preserve sharp pixel edges.
    
    :param input_path: Full path to the input image.
    :param output_path: Full path to save the output image (overwrites the input).
    :param target_size: The desired final dimensions (32x32).
    """
    try:
        # 1. Open the image (keeping original mode, including transparency)
        img = Image.open(input_path)

        # Skip files that aren't the expected source size (8x8)
        if img.size != SOURCE_TILE_SIZE:
            print(f"   -> SKIPPING: {input_path} (Size is {img.size}, expected {SOURCE_TILE_SIZE})")
            return

        # 2. Upscale using Nearest Neighbor (crucial for pixel art!)
        # This duplicates each pixel into a 4x4 block.
        upscaled_img = img.resize(target_size, Image.Resampling.NEAREST)

        # 3. Save the processed image, overwriting the original file.
        upscaled_img.save(output_path)
        print(f"   -> SUCCESS: Overwrote {input_path} with 32x32 upscaled version.")

    except Exception as e:
        print(f"   -> ERROR processing {input_path}: {e}")

def upscale_pixel_art_batch(root_dir):
    """
    Walks through the file system to find and upscale all 8x8 PNG files,
    saving them with their original names.
    """
    print(f"--- Starting pixel art upscaling batch from root directory: {os.path.abspath(root_dir)} ---")
    processed_count = 0
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for name in filenames:
            # Check for PNG files
            if name.lower().endswith('.png'):
                input_file_path = os.path.join(dirpath, name)
                
                # *** KEY CHANGE: Output path is the same as the input path ***
                output_file_path = input_file_path
                
                print(f"Checking file: {input_file_path}")
                
                # Process the image (will overwrite file if conditions met)
                upscale_image(input_file_path, output_file_path, TARGET_TILE_SIZE)
                processed_count += 1
    
    print(f"\n--- Batch upscaling complete. {processed_count} files checked. ---")

if __name__ == "__main__":
    # Ensure Pillow is installed: pip install Pillow
    upscale_pixel_art_batch(ROOT_DIR_TO_SCAN)