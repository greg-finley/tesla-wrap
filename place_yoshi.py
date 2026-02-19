"""
place_yoshi.py

Composites Yoshi sprites onto the left and right door panels of the
Tesla Model Y wrap template, centered within each door area.

Left door  → yoshi_90.png  (rotated so he's upright on the car)
Right door → yoshi_270.png (rotated so he's upright on the car)
"""

from PIL import Image
import numpy as np

TEMPLATE_PATH  = "template.png"
OUTPUT_PATH    = "outputs/yoshi_doors.png"
SKY_BLUE       = (100, 185, 255, 255)
LEFT_YOSHI     = "raw/sky_yoshi_90.png"
RIGHT_YOSHI    = "raw/sky_yoshi_270.png"

# Bounding boxes of the front door panels only (driver + front passenger)
# detected from the template's connected white regions
LEFT_DOOR  = dict(x0=30,  y0=284, x1=205, y1=544)
RIGHT_DOOR = dict(x0=821, y0=283, x1=997, y1=544)

# Scale Yoshi to this fraction of the door's smaller dimension
YOSHI_SCALE = 0.85


def place_sprite(canvas: Image.Image, sprite_path: str, door: dict) -> None:
    door_w = door["x1"] - door["x0"]
    door_h = door["y1"] - door["y0"]

    size = int(min(door_w, door_h) * YOSHI_SCALE)
    sprite = Image.open(sprite_path).convert("RGBA").resize((size, size), Image.LANCZOS)

    cx = door["x0"] + door_w // 2 - size // 2
    cy = door["y0"] + door_h // 2 - size // 2

    canvas.paste(sprite, (cx, cy), mask=sprite)


def main():
    template = Image.open(TEMPLATE_PATH).convert("RGBA")

    # Flood the entire background with sky blue
    data = np.array(template)
    white = (data[:,:,0] > 200) & (data[:,:,1] > 200) & (data[:,:,2] > 200)
    data[white] = SKY_BLUE
    template = Image.fromarray(data)

    place_sprite(template, LEFT_YOSHI,  LEFT_DOOR)
    place_sprite(template, RIGHT_YOSHI, RIGHT_DOOR)

    template.save(OUTPUT_PATH)
    print(f"Saved {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
