from PIL import Image, ImageEnhance
import os

# --- Configuration ---
# The script scans all subdirectories from the ROOT_DIR_TO_SCAN.
INPUT_SEARCH_PATTERN = "run_000.png"
OUTPUT_FILENAME_PATTERN = "teaser_16x16.png"
ROOT_DIR_TO_SCAN = "." # Start scan from the current directory (the root folder)

TARGET_LOW_RES = (16, 16) # The effective pixel data resolution
FINAL_DISPLAY_SIZE = (16, 16) # The actual size of the saved file
BRIGHTNESS_FACTOR = 0.15 # Reduces brightness; 0.15 is very dark

def process_single_image(input_path, output_path, size):
    """
    Core logic to convert an image to a dark, pixelated, transparent 16x16 teaser.
    
    :param input_path: Full path to the input image.
    :param output_path: Full path to save the output image.
    :param size: The final target dimensions (16x16).
    """
    try:
        # 1. Open the image and ensure RGBA mode for transparency preservation
        # This allows us to handle both color and the alpha channel.
        img = Image.open(input_path).convert('RGBA')

        # 2. Downscale the entire RGBA image to TARGET_LOW_RES (16x16)
        # LANCZOS is used for high-quality downsampling to condense color information.
        low_res_img = img.resize(TARGET_LOW_RES, Image.Resampling.LANCZOS)
        
        # Split the downscaled image into color (RGB) and transparency (A)
        r_low, g_low, b_low, a_low = low_res_img.split()
        low_res_rgb = Image.merge('RGB', (r_low, g_low, b_low))
        
        # 3. Convert only the color data to Greyscale ('L' mode)
        greyscale_img = low_res_rgb.convert('L')
        
        # 4. Darken the image significantly
        enhancer = ImageEnhance.Brightness(greyscale_img)
        darkened_img = enhancer.enhance(BRIGHTNESS_FACTOR)
        
        # 5. Convert darkened greyscale back to 3-channel RGB
        darkened_rgb = darkened_img.convert('RGB')
        
        # 6. Merge the darkened color data with the downscaled original alpha channel
        merged_low_res = Image.merge('RGBA', (*darkened_rgb.split(), a_low))
        
        # 7. Final resize using NEAREST filter for the chunky pixel effect
        # Resizing from 16x16 to 16x16 with NEAREST effectively just locks in
        # the distinct 16-pixel color palette for the final save.
        final_img = merged_low_res.resize(size, Image.Resampling.NEAREST)

        # 8. Save the processed image as PNG, which supports transparency
        final_img.save(output_path)
        print(f"   -> SUCCESS: Teaser saved at {output_path}")

    except Exception as e:
        # Using a more informative error message that includes the failing file path
        print(f"   -> ERROR processing {input_path}: {e}")

def create_pixelated_teasers_batch(root_dir):
    """
    Walks through the file system to find and process all 'run/run_000.png' images.
    """
    print(f"--- Starting batch processing from root directory: {os.path.abspath(root_dir)} ---")
    processed_count = 0
    
    # os.walk traverses the directory tree
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Check if the current directory is named 'run' AND contains the input file
        if os.path.basename(dirpath) == 'run' and INPUT_SEARCH_PATTERN in filenames:
            
            input_file_path = os.path.join(dirpath, INPUT_SEARCH_PATTERN)
            
            # Get the parent directory (one level up from 'run')
            parent_dir = os.path.dirname(dirpath)
            
            # Construct the output path in the parent directory
            output_file_path = os.path.join(parent_dir, OUTPUT_FILENAME_PATTERN)
            
            print(f"Processing found input: {input_file_path}")
            print(f"   Saving output to parent folder: {output_file_path}")
            
            # Use the single image processing function
            process_single_image(input_file_path, output_file_path, FINAL_DISPLAY_SIZE)
            processed_count += 1
    
    print(f"\n--- Batch processing complete. {processed_count} images processed. ---")

if __name__ == "__main__":
    # Ensure Pillow is installed: pip install Pillow
    create_pixelated_teasers_batch(ROOT_DIR_TO_SCAN)