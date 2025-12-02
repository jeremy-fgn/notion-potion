from PIL import Image
from pathlib import Path
import os
import sys
import subprocess

# --- Tile Filename Constants ---


BG = "background_black.png"
DOOR = "door_closed.png"
LOCKED = "door_locked.png"
FOOD = "edible_food.png"
POTION = "edible_potion.png"
BED = "furniture_bed.png"
CHEST = "furniture_chest.png"
JAIL = "furniture_jail.png"
TABLE = "furniture_table.png"
COIN = "item_coin.png"
KEY = "item_key.png"
DOG = "moving_animaldog.png"
KNIGHT = "moving_characterhelmet.png"
MONK = "moving_charactermonk.png"
PEASANT = "moving_characterpeasant.png"
SKEL = "moving_enemyskeleton.png"
SLIME = "moving_enemyslime.png"
SNAKE = "moving_enemysnake.png"
TROLL = "moving_enemytroll.png"
TREE = "nature_treeclassic.png"
PINE = "nature_treepine.png"
TROPI = "nature_treetropical.png"
FLOWER = "nature_flowers.png"
GRASS = "nature_grass.png"
RIVER = "nature_riversquiggle.png"
ROCK = "nature_rocks.png"
WATER = "nature_watersquare.png"
DUNG = "portal_dungeon.png"
HOLE = "portal_hole.png"
HOUSE = "portal_house.png"
HUT = "portal_hut.png"
FLAG = "portal_redflag.png"
GODOWN = "portal_stairsdown.png"
GOUP = "portal_stairsup.png"
ARROW = "prop_arrowright.png"
FIRE = "prop_bigfire.png"
HEART = "UI_heartfull.png"
PIRATE = "vehicle_pirateship.png"
RAFT = "vehicle_raft.png"
LWALL = "wall_left.png"
MWALL = "wall_middle.png"
RWALL = "wall_right.png"
TLWALL = "wall_topleft.png"
TRWALL = "wall_topright.png"
BLWALL = "wall_bottomleft.png"
BRWALL = "wall_bottomright.png"
AXE = "weapon_axe.png"
MACE = "weapon_bonk.png"
BOW = "weapon_bow.png"
SWORD = "weapon_sword.png"


# --- Configuration ---
WIDTH = 42  # Map width in tiles
TILE_DIM = 8  # Pixel dimensions of each source PNG (64x64)
OUTPUT_FILENAME = "collage.png"

raw_map_data = [
    1 * [BG],
    1 * [BG],
    1 * [BG],
    1 * [BG],

    # Row 1: Open forest floor with a rocky/pine cluster and a solitary tree
    16 * [BG] + [FLOWER] + [BG] + [ROCK] + [PINE] + 3 * [BG] + [ROCK] + [BG] + [PINE] + 3 * [BG] + [TREE] + [PINE],

    # Row 2: Dense forest line with rocks, trees, and a flower
    14 * [BG] + [ROCK] + 5 * [BG] + [TREE] + [FLOWER] + 3 * [BG] + [TREE] + [BG] + [ROCK] + [PINE] + 3 * [ROCK] + [BG] + [PINE],

    # Row 3: Rocky patch transitioning into an area with trees and scattered flowers
    15 * [BG] + [ROCK] + [BG] + [TREE] + [BG] + [ROCK] + 2 * [BG] + [FLOWER] + 2 * [BG] + [FLOWER] + 2 * [BG] + [ROCK] + [PINE] + 4 * [BG] + [ROCK],

    # Row 4: Top perimeter of the building, with a skeleton and rocks outside
    11 * [BG] + [ROCK] + [SKEL] + [ROCK] + 3 * [BG] + [TREE] + 2 * [BG] + [TLWALL] + 8 * [MWALL] + [TRWALL] + 3 * [MWALL] + [TRWALL],

    # Row 5: Building's right side wall, with a chest inside
    21 * [BG] + 8 * [BG] + [RWALL] + [BG] + [CHEST] + [BG] + [RWALL],

    # Row 6: Building's lower right side wall, with a snake, potion, and a troll outside
    20 * [BG] + [LWALL] + 6 * [BG] + [SNAKE] + [POTION] + [RWALL] + [BG] + [TROLL] + [BG] + [RWALL],

    # Row 7: Building's base and a bottom wall structure with a locked door
    20 * [BG] + 4 * [MWALL] + [LOCKED] + 4 * [MWALL] + [RWALL] + [MWALL] + [DOOR] + [MWALL] + [RWALL],

    3 * [BG] + 5 * [GRASS] + 5 * [BG] + 15 * [WATER] + 5 * [GRASS] + 5 * [BG], # Total: 33 items, pads to 42

    3 * [FLOWER] + 7 * [GRASS] + 18 * [WATER] + 5 * [GRASS], # Total: 33 items, pads to 42

    3 * [FLOWER] + 4 * [GRASS] + 20 * [WATER] + [TROLL] + 5 * [GRASS], # Total: 33 items, pads to 42

    2 * [TREE] + 5 * [GRASS] + 17 * [WATER] + [BG] + 5 * [GRASS], # Total: 30 items, pads to 42

    10 * [GRASS] + [BG] + [TROLL] + 2 * [BG] + [FIRE] + 2 * [BG] + [TROLL] + [BG] + 5 * [ROCK] + 5 * [BG], # Total: 30 items, pads to 42

    8 * [GRASS] + 5 * [ROCK] + 5 * [BG] + [TROLL] + 2 * [BG] + [FIRE] + 2 * [BG] + [TROLL] + 5 * [BG], # Total: 30 items, pads to 42

    15 * [GRASS] + 5 * [BG] + 5 * [TREE] + 5 * [BG], # Total: 30 items, pads to 42

    20 * [GRASS] + [ARROW] + 5 * [TREE] + 5 * [BG], # Total: 31 items, pads to 42

    5 * [TREE] + 10 * [GRASS] + 5 * [TREE] + 5 * [GRASS] + 5 * [BG], # Total: 30 items, pads to 42

    3 * [PINE] + 5 * [TREE] + 5 * [PINE] + 5 * [GRASS] + 5 * [BG], # Total: 23 items, pads to 42

    15 * [BG] + [ROCK] + 5 * [BG] + [ROCK] + 10 * [BG] + [MONK], # Total: 37 items, pads to 42

    2 * [BG] + 10 * [ROCK] + 5 * [BG] + 5 * [ROCK] + 15 * [BG], # Total: 37 items, pads to 42

    4 * [BG] + 5 * [ROCK] + 5 * [BG] + 5 * [TREE] + 5 * [BG] + 5 * [ROCK] + 10 * [BG], # Total: 39 items, pads to 42

    2 * [TREE] + 5 * [PINE] + 5 * [BG] + 10 * [GRASS] + 5 * [BG] + 5 * [TREE] + 5 * [BG], # Total: 37 items, pads to 42

    3 * [TREE] + 10 * [GRASS] + 5 * [WATER] + 10 * [GRASS] + 5 * [TREE], # Total: 33 items, pads to 42

    5 * [GRASS] + 10 * [WATER] + 5 * [GRASS] + 10 * [WATER] + 5 * [GRASS], # Total: 35 items, pads to 42

    10 * [WATER] + 5 * [GRASS] + 5 * [WATER] + 5 * [GRASS] + 5 * [WATER] + 5 * [GRASS], # Total: 35 items, pads to 42

    5 * [BG] + 5 * [ROCK] + 20 * [GRASS] + 5 * [ROCK] + 5 * [BG], # Total: 40 items, pads to 42

    15 * [BG] + [FLOWER] + 5 * [BG] + [FLOWER] + 15 * [BG], # Total: 37 items, pads to 42

    10 * [BG] + 5 * [TREE] + 10 * [BG] + 5 * [PINE] + 5 * [BG], # Total: 35 items, pads to 42

    1 * [BG],
    1 * [BG],
    1 * [BG],
    1 * [BG]

]

# --- 2. Process Map and Generate Image ---

# 3. Trim or pad lines to ensure they are exactly WIDTH tiles wide
# Note: The loop now naturally processes all lines in raw_map_data.
processed_map = []
for i, line in enumerate(raw_map_data):
    if len(line) > WIDTH:
        # Trim excess tiles
        processed_line = line[:WIDTH]
        print(f"Warning: Line {i+1} was trimmed from {len(line)} to {WIDTH} tiles.")
    elif len(line) < WIDTH:
        # Pad with the background tile
        padding = (WIDTH - len(line)) * [BG]
        processed_line = line + padding
        print(f"Info: Line {i+1} was padded from {len(line)} to {WIDTH} tiles.")
    else:
        processed_line = line
    
    processed_map.append(processed_line)

# Calculate final canvas dimensions
canvas_width = WIDTH * TILE_DIM
canvas_height = len(processed_map) * TILE_DIM

# Create the final collage image
try:
    # Initialize the final collage image
    collage = Image.new('RGB', (canvas_width, canvas_height))
    
    # Iterate through the processed map data (row by row, tile by tile)
    for y_index, row in enumerate(processed_map):
        for x_index, filename in enumerate(row):
            # Open the tile image
            try:
                # Open the image and convert it to RGB (important for merging)
                tile_image = Image.open(filename).convert("RGB")
                
                # Check and resize if tile is not the correct size (64x64)
                if tile_image.size != (TILE_DIM, TILE_DIM):
                     print(f"Warning: {filename} is {tile_image.size}, expected {TILE_DIM}x{TILE_DIM}. Resizing.")
                     tile_image = tile_image.resize((TILE_DIM, TILE_DIM))
                         
            except FileNotFoundError:
                print(f"Error: Tile file '{filename}' not found. Using black background.")
                # Use a black placeholder tile if the file is missing
                tile_image = Image.new('RGB', (TILE_DIM, TILE_DIM), color='#000000')
            
            # Calculate the top-left corner position for placing the tile
            x_pos = x_index * TILE_DIM
            y_pos = y_index * TILE_DIM
            
            # Paste the tile onto the collage
            collage.paste(tile_image, (x_pos, y_pos))

    # 4. Save the final image
    collage.save(OUTPUT_FILENAME)
    print(f"\n✅ Image successfully generated and saved as '{OUTPUT_FILENAME}'")

except ImportError:
    print("\nError: The 'Pillow' library is not installed.")
    print("Please install it by running: pip install Pillow")
except Exception as e:
    print(f"\nAn unexpected error occurred during image generation: {e}")

# --- Upscaling to 2x (16x16 pixels per tile) ---

# Define the new, upscaled filename
OUTPUT_2X_FILENAME = "collage_2x.png"

# Calculate the new dimensions
new_width_2x = canvas_width * 2
new_height_2x = canvas_height * 2

print(f"\nUpscaling to 2x: {new_width_2x}x{new_height_2x} pixels...")

# Resize the collage using the NEAREST filter. 
# This is crucial as it prevents blending/blurring and keeps the pixel-art sharp.
collage_2x = collage.resize(
    (new_width_2x, new_height_2x), 
    resample=Image.Resampling.NEAREST  # Use NEAREST for perfect pixel doubling
)

# Save the 2x image
collage_2x.save(OUTPUT_2X_FILENAME)

print(f"✅ 2x Upscaled image saved as '{OUTPUT_2X_FILENAME}'")
# --- AUTO-OPEN THE FILE ---
try:
    if os.name == 'nt':  # Windows
        subprocess.run(['start', OUTPUT_2X_FILENAME], shell=True, check=True)
    elif sys.platform == 'darwin':  # macOS
        subprocess.run(['open', OUTPUT_2X_FILENAME], check=True)
    else:  # Linux (uses 'xdg-open' for most desktop environments)
        subprocess.run(['xdg-open', OUTPUT_2X_FILENAME], check=True)
    
    print(f"Opening '{OUTPUT_2X_FILENAME}' in default viewer...")

except Exception as e:
    print(f"Could not automatically open the file: {e}")
# ---------------------------