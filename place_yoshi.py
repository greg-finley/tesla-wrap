"""
place_yoshi.py

Composites Yoshi sprites onto the Tesla Model Y wrap template.

Left door  → yoshi_90.png       (rotated so he's upright on the car)
Right door → yoshi_270.png      (rotated so he's upright on the car)
Trunk      → yoshi_egg.png      (centered on rear trunk panel, 1.5x scale)
Frunk      → yoshi_face_180.png (upside-down face on front hood)
"""

from PIL import Image
import numpy as np

TEMPLATE_PATH  = "template.png"
OUTPUT_PATH    = "outputs/yoshi_doors.png"
SKY_BLUE       = (100, 185, 255, 255)
LEFT_YOSHI     = "raw/sky_yoshi_90.png"
RIGHT_YOSHI    = "raw/sky_yoshi_270.png"
TRUNK_EGG      = "raw/sky_yoshi_egg.png"
FRUNK_FACE     = "raw/sky_yoshi_face_180.png"  # upside-down

# Bounding boxes of the front door panels only (driver + front passenger)
# detected from the template's connected white regions
LEFT_DOOR  = dict(x0=30,  y0=284, x1=205, y1=544)
RIGHT_DOOR = dict(x0=821, y0=283, x1=997, y1=544)
TRUNK      = dict(x0=352, y0=800, x1=671, y1=940, scale=1.0)  # 1x scale
FRUNK      = dict(x0=409, y0=165, x1=615, y1=215, scale=3.0)  # fill most of panel

# Scale Yoshi to this fraction of the door's smaller dimension
YOSHI_SCALE = 0.85


def place_sprite(canvas: Image.Image, sprite_path: str, door: dict) -> None:
    door_w = door["x1"] - door["x0"]
    door_h = door["y1"] - door["y0"]

    scale = door.get("scale", 1.0) * YOSHI_SCALE
    base_size = int(min(door_w, door_h) * scale)

    sprite = Image.open(sprite_path).convert("RGBA")
    # Maintain aspect ratio
    aspect = sprite.width / sprite.height
    if aspect > 1:  # wider than tall
        w = base_size
        h = int(base_size / aspect)
    else:  # taller than wide or square
        h = base_size
        w = int(base_size * aspect)

    sprite = sprite.resize((w, h), Image.LANCZOS)

    cx = door["x0"] + door_w // 2 - w // 2
    cy = door["y0"] + door_h // 2 - h // 2

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
    place_sprite(template, TRUNK_EGG,   TRUNK)
    place_sprite(template, FRUNK_FACE,  FRUNK)

    template.save(OUTPUT_PATH)
    print(f"Saved {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
