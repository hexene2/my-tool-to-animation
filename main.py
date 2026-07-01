from PIL import Image, ImageDraw
import os
import subprocess

# ------------------------
# Settings
# ------------------------
WIDTH = 1280
HEIGHT = 1280
FPS = 60 
DURATION = 3  # seconds

FRAME_COUNT = FPS * DURATION
OUTPUT_DIR = "frames"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ------------------------
# Generate Frames
# ------------------------
for frame in range(FRAME_COUNT):

    # Create black background
    img = Image.new("RGB", (WIDTH, HEIGHT), "white")
    draw = ImageDraw.Draw(img)

    # Animate line growing
    progress = frame / FRAME_COUNT

    x1 = 200
    y1 = HEIGHT // 3

    x2 = int(200 + progress * 800)
    y2 = (HEIGHT // 3)*2

    #draw.line((x1, y1, x2, y2), fill="white", width=8)
    coordinates = (x1 ,y1 ,x2 ,y2)
    draw.rectangle(coordinates, fill="yellow", outline="blue", width=3)
    img.save(f"{OUTPUT_DIR}/{frame:05d}.png")

# ------------------------
# Convert to MP4
# ------------------------
subprocess.run([
    "ffmpeg",
    "-y",
    "-framerate", str(FPS),
    "-i", f"{OUTPUT_DIR}/%05d.png",
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    "output.mp4"
])
