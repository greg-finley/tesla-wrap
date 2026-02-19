from PIL import Image
import numpy as np

img = Image.open("template.png").convert("RGBA")
data = np.array(img)

# Find near-white pixels (R, G, B all > 200)
white_mask = (data[:, :, 0] > 200) & (data[:, :, 1] > 200) & (data[:, :, 2] > 200)

# Replace with purple (128, 0, 128, 255)
data[white_mask] = [128, 0, 128, 255]

result = Image.fromarray(data)
result.save("template_purple.png")
print("Saved template_purple.png")
