"""
yoshi_scene.py

Applies a Yoshi's Island side-scrolling scene to the LEFT panels of the
Tesla Model Y wrap template.

IMPORTANT — panel orientation:
  The left panels in template.png are laid out horizontally (rotated 90° CCW
  relative to how they sit on the actual car). Art is drawn upright, then
  rotated 90° CW before being stamped onto the template so it looks
  right-side-up on the real door.

Only pixels that are:
  - In the LEFT region of the image (x < LEFT_BOUNDARY)
  - Part of a panel (near-white in the template)
are modified. Middle and right panels are untouched.
"""

from PIL import Image, ImageDraw
import numpy as np

# ── Config ────────────────────────────────────────────────────────────────────

TEMPLATE_PATH = "template.png"
OUTPUT_PATH = "outputs/yoshi_scene_left.png"

# Pixel x-coordinate cutoff: anything left of this is considered a left panel.
# Adjust if the boundary doesn't line up with the template.
LEFT_BOUNDARY = 230  # right edge of left panels (tightened to avoid center strips)

# "Near-white" threshold for detecting panel regions in the template
WHITE_THRESHOLD = 200

# ── Scene painter ─────────────────────────────────────────────────────────────

GROUND_FRACTION = 0.15  # ground takes up this fraction of the scene height

def make_yoshi_scene(width: int, height: int) -> Image.Image:
    """
    Generate a simple sky + ground scene at (width x height).
    Drawn upright — will be rotated 90° CW before application.
    """
    scene = Image.new("RGBA", (width, height))
    draw = ImageDraw.Draw(scene)

    sky_blue     = (100, 185, 255, 255)
    ground_green = (80,  160,  40, 255)

    horizon = int(height * (1.0 - GROUND_FRACTION))

    draw.rectangle([0, 0, width, horizon], fill=sky_blue)
    draw.rectangle([0, horizon, width, height], fill=ground_green)

    return scene


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    template = Image.open(TEMPLATE_PATH).convert("RGBA")
    data = np.array(template)
    result = data.copy()

    img_h, img_w = data.shape[:2]

    # Build a mask: left-region panels (near-white pixels left of boundary)
    left_region = np.zeros((img_h, img_w), dtype=bool)
    left_region[:, :LEFT_BOUNDARY] = True

    white_mask = (
        (data[:, :, 0] > WHITE_THRESHOLD) &
        (data[:, :, 1] > WHITE_THRESHOLD) &
        (data[:, :, 2] > WHITE_THRESHOLD)
    )
    panel_mask = white_mask & left_region

    # Bounding box of left panel region
    rows = np.where(panel_mask.any(axis=1))[0]
    cols = np.where(panel_mask.any(axis=0))[0]
    if len(rows) == 0 or len(cols) == 0:
        print("No left panel pixels found — check LEFT_BOUNDARY value.")
        return

    r0, r1 = rows[0], rows[-1]
    c0, c1 = cols[0], cols[-1]
    bh = r1 - r0 + 1
    bw = c1 - c0 + 1

    print(f"Left panel bounding box: x={c0}–{c1}, y={r0}–{r1}  ({bw}×{bh}px)")

    # Generate scene upright at bounding-box size, then rotate 90° CW
    # 90° CW: scene width → bh, scene height → bw  (dims swap after rotation)
    scene = make_yoshi_scene(bh, bw)          # draw at (tall × wide)
    scene_rot = scene.rotate(-90, expand=True) # rotate CW → now (bw × bh)
    scene_arr = np.array(scene_rot)           # shape: (bh, bw, 4)

    # Stamp scene pixels only where the panel mask is True
    crop_mask = panel_mask[r0:r1+1, c0:c1+1]
    region = result[r0:r1+1, c0:c1+1]
    region[crop_mask] = scene_arr[crop_mask]
    result[r0:r1+1, c0:c1+1] = region

    out = Image.fromarray(result)
    out.save(OUTPUT_PATH)
    print(f"Saved {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
