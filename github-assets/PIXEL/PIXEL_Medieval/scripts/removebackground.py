from PIL import Image
import os

# --- Configuration ---
# The target black background color (R, G, B)
TARGET_COLOR = (35, 34, 35) 
# Tolerance for color matching (plus or minus)
COLOR_TOLERANCE = 5 
# --- End Configuration ---

def is_close(color1_component, color2_component, tolerance):
    """Checks if two color components are within the given tolerance."""
    return abs(color1_component - color2_component) <= tolerance

def process_image(filepath):
    """
    Opens an image, removes the background to transparent, 
    and saves the new image, overwriting the original file.
    """
    try:
        # 1. Open the image
        img = Image.open(filepath)
        
        # Ensure the image has an alpha channel for transparency operations
        # Convert to RGBA if not already
        if img.mode != 'RGBA':
            img = img.convert('RGBA')

        # Get the pixel data
        data = img.getdata()
        
        new_data = []

        # Target components for easier comparison
        tr, tg, tb = TARGET_COLOR
        
        print(f"Processing and overwriting {os.path.basename(filepath)}...")

        # 2. Iterate through all pixels
        for item in data:
            r, g, b, a = item
            
            # Check if the pixel color is within the tolerance range of the target black
            if (is_close(r, tr, COLOR_TOLERANCE) and
                is_close(g, tg, COLOR_TOLERANCE) and
                is_close(b, tb, COLOR_TOLERANCE)):
                
                # Match found: set alpha channel (A) to 0 (fully transparent)
                new_data.append((r, g, b, 0))
                
            else:
                # No match: keep the original pixel data
                new_data.append(item)

        # 3. Create the new image with the transparent background
        img_transparent = Image.new('RGBA', img.size)
        img_transparent.putdata(new_data)
        
        # 4. Save the new image, overwriting the original file
        # Note: Saving an RGBA image as PNG preserves transparency automatically
        img_transparent.save(filepath)
        print(f"   -> Successfully overwritten with transparent background: {filepath}")

    except Exception as e:
        print(f"Error processing {filepath}: {e}")

def main():
    """Main function to find and process all PNG files."""
    
    # Iterate through all files in the current directory
    for filename in os.listdir('.'):
        # Only process PNG files
        if filename.lower().endswith('.png'):
            process_image(filename)

if __name__ == "__main__":
    # WARNING: This script overwrites your original PNG files!
    main()