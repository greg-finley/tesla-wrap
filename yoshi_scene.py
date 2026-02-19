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
LEFT_BOUNDARY = 340  # roughly the left third of a 1024-wide image

# "Near-white" threshold for detecting panel regions in the template
WHITE_THRESHOLD = 200

# ── Scene painter ─────────────────────────────────────────────────────────────

def make_yoshi_scene(width: int, height: int) -> Image.Image:
    """
    Generate a Yoshi's Island side-scrolling scene at (width x height).
    Drawn upright — will be rotated 90° CW before application.
    """
    scene = Image.new("RGBA", (width, height))
    draw = ImageDraw.Draw(scene)

    sky_blue    = (100, 185, 255, 255)
    ground_green= (80,  160,  40, 255)
    hill_green  = (60,  140,  30, 255)
    pipe_green  = (0,   140,   0, 255)
    pipe_dark   = (0,   100,   0, 255)
    cloud_white = (255, 255, 255, 220)
    coin_yellow = (255, 210,   0, 255)
    egg_white   = (240, 240, 240, 255)
    egg_spot    = (80,  200,  80, 255)

    horizon = int(height * 0.65)

    # Sky
    draw.rectangle([0, 0, width, horizon], fill=sky_blue)

    # Ground
    draw.rectangle([0, horizon, width, height], fill=ground_green)

    # Rolling hills
    hill_points = [
        (0, horizon),
        (width * 0.15, horizon - height * 0.18),
        (width * 0.32, horizon),
        (width * 0.55, horizon - height * 0.25),
        (width * 0.75, horizon),
        (width * 0.90, horizon - height * 0.12),
        (width, horizon),
        (width, height),
        (0, height),
    ]
    draw.polygon([(int(x), int(y)) for x, y in hill_points], fill=hill_green)

    # Clouds (simple overlapping circles)
    def draw_cloud(cx, cy, r):
        for dx, dy, rr in [(-r, 0, r), (0, -int(r*0.7), int(r*0.8)),
                            (r, 0, r), (0, 0, int(r*1.1))]:
            draw.ellipse([cx+dx-rr, cy+dy-rr, cx+dx+rr, cy+dy+rr],
                         fill=cloud_white)

    draw_cloud(int(width * 0.12), int(height * 0.15), int(height * 0.07))
    draw_cloud(int(width * 0.48), int(height * 0.10), int(height * 0.09))
    draw_cloud(int(width * 0.80), int(height * 0.18), int(height * 0.06))

    # Warp pipe (left side)
    pw = int(width * 0.10)
    ph = int(height * 0.28)
    px = int(width * 0.08)
    py = horizon - ph
    cap_h = int(ph * 0.15)
    draw.rectangle([px, py + cap_h, px + pw, horizon], fill=pipe_green)
    draw.rectangle([px - int(pw * 0.1), py, px + pw + int(pw * 0.1), py + cap_h],
                   fill=pipe_green)
    draw.rectangle([px + pw - int(pw * 0.2), py + cap_h,
                    px + pw, horizon], fill=pipe_dark)

    # Warp pipe (right side, shorter)
    pw2 = int(width * 0.09)
    ph2 = int(height * 0.18)
    px2 = int(width * 0.82)
    py2 = horizon - ph2
    draw.rectangle([px2, py2 + cap_h, px2 + pw2, horizon], fill=pipe_green)
    draw.rectangle([px2 - int(pw2 * 0.1), py2,
                    px2 + pw2 + int(pw2 * 0.1), py2 + cap_h], fill=pipe_green)
    draw.rectangle([px2 + pw2 - int(pw2 * 0.2), py2 + cap_h,
                    px2 + pw2, horizon], fill=pipe_dark)

    # Coins in an arc
    coin_r = int(width * 0.025)
    for i, (cx_frac, cy_frac) in enumerate([
        (0.38, 0.42), (0.44, 0.36), (0.50, 0.33),
        (0.56, 0.36), (0.62, 0.42),
    ]):
        cx = int(width * cx_frac)
        cy = int(height * cy_frac)
        draw.ellipse([cx - coin_r, cy - coin_r, cx + coin_r, cy + coin_r],
                     fill=coin_yellow)

    # Yoshi egg on the ground (center-right)
    ex = int(width * 0.65)
    ey = horizon - int(height * 0.12)
    ew = int(width * 0.11)
    eh = int(height * 0.14)
    draw.ellipse([ex, ey, ex + ew, ey + eh], fill=egg_white)
    # Spots
    spot_r = int(ew * 0.15)
    for sx, sy in [(ex + int(ew*0.25), ey + int(eh*0.25)),
                   (ex + int(ew*0.65), ey + int(eh*0.20)),
                   (ex + int(ew*0.45), ey + int(eh*0.55))]:
        draw.ellipse([sx - spot_r, sy - spot_r, sx + spot_r, sy + spot_r],
                     fill=egg_spot)

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
