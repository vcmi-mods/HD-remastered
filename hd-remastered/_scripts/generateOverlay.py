#!/usr/bin/env python3

import sys
from pathlib import Path
from PIL import Image

def extract_flag_overlay_from_yellow(folder_path):
    folder = Path(folder_path)
    yellow = (255, 255, 0)

    if not folder.exists():
        print(f"[ERROR] Folder does not exist: {folder}")
        return

    png_files = list(folder.rglob("*.png"))
    if not png_files:
        print("[INFO] No PNG files found.")
        return

    for png_file in png_files:
        if "-overlay" in png_file.stem or "-shadow" in png_file.stem:
            continue  # Skip overlay or shadow files

        img = Image.open(png_file).convert("RGBA")
        overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        pixels = img.load()
        overlay_pixels = overlay.load()

        found = False

        for y in range(img.height):
            for x in range(img.width):
                r, g, b, a = pixels[x, y]
                if (r, g, b) == yellow and a > 0:
                    overlay_pixels[x, y] = (255, 255, 255, 255)
                    found = True

        if found:
            output_path = png_file.with_name(png_file.stem + "-overlay.png")
            overlay.save(output_path)
            print(f"[OK] Created overlay: {output_path.name}")
        else:
            print(f"[SKIP] No yellow found in: {png_file.name}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_flag_overlay.py <folder_with_png>")
        sys.exit(1)

    folder = sys.argv[1]
    extract_flag_overlay_from_yellow(folder)
