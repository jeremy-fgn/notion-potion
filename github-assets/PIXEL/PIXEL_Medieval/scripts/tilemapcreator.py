from PIL import Image
import os
from PIL.Image import Resampling # Required for PIL resize methods

# --- 1. Tile Filename Constants (The "Legend") ---
# IMPORTANT: These files MUST exist in the same directory as this script,
# and they must be 32x32 pixels, or they will be resized/fail.
BG = "background_black.png"
FLOWER = "nature_flowers.png"
ROCK = "nature_rocks.png"
TREE = "nature_treeclassic.png"
PINE = "nature_treepine.png"
BOSS = "boss.png"
MISSING_TILE_COLOR = '#000000' # Black color for missing tiles

# --- 2. Configuration ---
TILE_DIM = 32      # Pixel dimensions of each source tile (32x32)
OUTPUT_FILENAME = "collage.png"


# --- 3. Manually Defined Tilemap (The "Map Data") ---
# This is a list of lists, where each inner list is a row of the map.
# Each item corresponds to one TILE_DIM x TILE_DIM area on the final image.
MAP_DATA = [
    # X=0   X=1   X=2   X=3   X=4   X=5   X=6   X=7   X=8   X=9 
    [BG,    BG,   BG,   BG,   BG,   BG,   BG,   BG,   BG,   BG],  # Y=0
    [BG,    TREE, BG,   BG,   ROCK, BG,   BG,   BG,   PINE, BG],  # Y=1
    [BG,    BG,   BG,   FLOWER, BG,  BG,   BG,   BG,   BG,   BG],  # Y=2
    [BOSS,  BG,   BG,   BG,   BG,   BG,   ROCK, BG,   BG,   BG],  # Y=3
]

# --- 4. Core Logic ---

try:
    # Calculate map dimensions
    MAP_WIDTH = len(MAP_DATA[0])
    MAP_HEIGHT = len(MAP_DATA)

    # Calculate final canvas dimensions in pixels
    canvas_width = MAP_WIDTH * TILE_DIM
    canvas_height = MAP_HEIGHT * TILE_DIM
    
    print(f"Generating image: {MAP_WIDTH} tiles wide x {MAP_HEIGHT} tiles high.")
    print(f"Final size: {canvas_width}px x {canvas_height}px.")

    # Initialize the final collage image (using RGB mode)
    collage = Image.new('RGB', (canvas_width, canvas_height))
    
    # Iterate through the map data, row by row (y_index) and tile by tile (x_index)
    for y_index, row in enumerate(MAP_DATA):
        for x_index, filename in enumerate(row):
            # Calculate the top-left corner position for placing the tile
            x_pos = x_index * TILE_DIM
            y_pos = y_index * TILE_DIM
            
            # --- Load and Place Tile ---
            try:
                # 1. Open the image and ensure it's RGB
                tile_image = Image.open(filename).convert("RGB")
                
                # 2. Check and resize if the tile is not the correct size
                if tile_image.size != (TILE_DIM, TILE_DIM):
                    print(f"Warning: '{filename}' is {tile_image.size}. Resizing to {TILE_DIM}x{TILE_DIM}.")
                    # Use Resampling.NEAREST to preserve sharp pixel art if resizing is needed
                    tile_image = tile_image.resize((TILE_DIM, TILE_DIM), Resampling.NEAREST)
                    
            except FileNotFoundError:
                # 3. Simple error handling: Use a black placeholder if file is missing
                print(f"Error: Tile file '{filename}' not found. Using black placeholder.")
                tile_image = Image.new('RGB', (TILE_DIM, TILE_DIM), color=MISSING_TILE_COLOR)
                
            # 4. Paste the tile onto the collage at the calculated position
            collage.paste(tile_image, (x_pos, y_pos))

    # 5. Save the final image
    collage.save(OUTPUT_FILENAME)
    print(f"\n✅ Success! Tilemap image saved as '{OUTPUT_FILENAME}'")

except ImportError:
    print("\nError: The 'Pillow' library is not installed.")
    print("Please install it by running: pip install Pillow")
except Exception as e:
    # General catch-all for other OS/file issues
    print(f"\nAn unexpected error occurred during image generation: {e}")