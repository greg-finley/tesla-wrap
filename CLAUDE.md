# Tesla Model Y Wrap Designer

This project is for designing vinyl wraps for a Tesla Model Y.

## Files

- `template.png` — flat-lay outline template of the Tesla Model Y showing all panels (roof, doors, fenders, bumpers, etc.)
- `place_yoshi.py` — main script to composite Yoshi sprites onto the template with sky blue background
- `colorize.py` — legacy script to apply colors/fills to the template
- `raw/` — source sprite images (both original and sky-blue processed versions with `sky_` prefix)
- `outputs/` — completed wrap designs

## Panel Orientation Note

The template is a flat-lay top-down unfolded view. The left and right door/fender panels
are laid out horizontally in the image, but they are **vertical on the actual car**.

**Any artwork placed on the left panels must be rotated 90 degrees clockwise** so it
appears right-side-up when the wrap is applied to the car door. The same applies
(mirrored) for right panels.

Only work on left panels unless explicitly asked to touch middle or right panels.

## Sprite Processing Workflow

When adding new sprites to the wrap design:

1. **Sky Blue Background**: Replace transparent or white backgrounds with sky blue `(100, 185, 255)`
   - For images with alpha channel: replace pixels where `alpha < 128` with sky blue
   - For images with white background: replace near-white pixels (`R,G,B > 200`) with sky blue
   - Save processed sprites with `sky_` prefix (e.g., `sky_yoshi_face.png`)

2. **Tight Cropping**: Remove excess sky blue borders from sprites
   - Detect non-sky-blue pixels: `abs(R-100) > 5 OR abs(G-185) > 5 OR abs(B-255) > 5`
   - Find bounding box of content pixels
   - Crop to tight bounds to maximize sprite size when placed on panels

3. **Multiple Orientations**: For non-symmetric sprites, generate rotated versions
   - Use `-90` suffix for 90° CW rotation (for left/vertical panels)
   - Use `-180` suffix for 180° rotation (upside-down)
   - Use `-270` suffix for 270° CW rotation (for right/vertical panels)

## Git Workflow

Commit regularly throughout a session — after adding new scripts, after meaningful changes
to existing scripts, and after generating notable outputs. Don't wait until the end.
Each commit should capture one logical step so the history is easy to follow.

## Outputs

Previous designs saved in `outputs/`:
- `mutt_cutts_wrap.png`
- `template_purple.png`
- `tesla_dog_skin.png`
- `tesla_skin_v4.png`
- `tiger_dog_car.png`
