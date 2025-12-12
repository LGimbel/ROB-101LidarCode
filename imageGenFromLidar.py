import time
from PIL import Image
from typing import List

IMAGE_WIDTH = 360
IMAGE_HEIGHT = 1
MAX_DISTANCE_VALUE = 300 # Max value used for scaling color (1-200)

CSV_DATA_STRING = "3,3,3,3,2,3,2,3,4,1,2,2,3,3,3,3,3,3,4,5,6,7,8,8,9,10,11,12,13,13,14,20,21,21,21,21,21,28,28,28,28,29,29,29,29,33,24100,35,38,38,46,47,47,47,48,49,50,54,55,56,57,57,57,57,58,57,57,57,58,62,64,66,66,67,68,67,68,68,69,71,74,76,78,78,83,84,84,84,84,84,86,87,89,90,90,91,91,91,91,92,92,94,95,96,97,97,97,97,98,98,99,99,99,100,100,100,100,100,100,101,101,101,102,102,103,103,103,103,103,103,103,103,105,104,105,105,104,106,106,107,107,107,107,109,107,107,108,108,108,110,109,110,110,110,110,110,110,110,111,111,113,113,114,114,115,116,116,116,117,116,116,118,117,118,118,117,118,118,118,119,118,118,119,120,120,119,121,122,122,122,122,122,122,123,122,123,123,123,123,123,124,125,125,125,125,126,126,126,127,128,129,128,128,127,127,129"

def map_value_to_color(value: int) -> tuple:
    """
    Maps a distance value (1-200) to an RGB color based on a Red-to-Blue gradient.
    Closest (value=1) -> Red.
    Farthest (value=200) -> Blue.
    """
    value = max(1, min(MAX_DISTANCE_VALUE, value))
    
    t = (value - 1) / (MAX_DISTANCE_VALUE - 1)
    
    R = int((1.0 - t) * 255)
    B = int(t * 255)
    G = 0
    
    return (R, G, B)

def parse_csv_string(csv_string: str) -> List[int]:
    """Converts the comma-separated string into a list of integers."""
    try:
        str_values = csv_string.split(',')
        data_array = [int(v.strip()) for v in str_values if v.strip().isdigit()]
        return data_array
    except ValueError as e:
        print(f"[ERROR] Error during data parsing: {e}")
        return []

def create_image_from_data(data_array: List[int]):
    """Creates a 1x360 image from the list of distance values."""
    
    img_width = len(data_array) 
    
    if img_width == 0:
        print("Error: Data array is empty. Image creation skipped.")
        return

    print(f"Creating {img_width}x{IMAGE_HEIGHT} color image...")
    
    img = Image.new('RGB', (img_width, IMAGE_HEIGHT))
    pixels = img.load() 

    for x in range(img_width):
        distance = data_array[x]
        color = map_value_to_color(distance)
        pixels[x, 0] = color 

    filename = f'lidar_scan_hardcoded_color_{int(time.time())}.png'
    img.save(filename)
    print(f"\n[SUCCESS] Image saved as '{filename}'.")


def main():
    data_to_process = parse_csv_string(CSV_DATA_STRING)
    
    if data_to_process:
        create_image_from_data(data_to_process)


if __name__ == '__main__':
    main()