#!/usr/bin/env python3

import sys
import os
import json
import warnings
import logging
from pathlib import Path
from tkinter import Tk, messagebox
from tkinter.filedialog import askopenfilenames

from homm3data import deffile

# === Logging (only activated if needed) ===
logger_initialized = False
script_dir = Path(__file__).parent
log_path = script_dir / "def2json.log"

def ensure_logger():
    global logger_initialized
    if not logger_initialized:
        logging.basicConfig(
            filename=log_path,
            level=logging.INFO,
            format='[%(levelname)s] %(asctime)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        logger_initialized = True

def custom_warning(message, category, filename, lineno, file=None, line=None):
    ensure_logger()
    logging.warning(f"{filename}:{lineno} {category.__name__}: {message}")

warnings.showwarning = custom_warning


def process_def_default(path):
    foldername = os.path.dirname(path)
    filename = os.path.basename(path)

    output_dir = os.path.join(foldername, Path(filename).stem)
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    tmp_json = {"images": [], "basepath": Path(filename).stem + "/"}

    with deffile.open(path) as d:
        for group in d.get_groups():
            for frame in range(d.get_frame_count(group)):
                frame_base_name = d.get_image_name(group, frame)
                tmp_json["images"].append({
                    "group": group,
                    "frame": frame,
                    "file": f"{frame_base_name}.png"
                })

                img = d.read_image('normal', group, frame)
                img.save(os.path.join(output_dir, f"{frame_base_name}.png"))

                img = d.read_image('shadow', group, frame)
                if img is not None:
                    img.save(os.path.join(output_dir, f"{frame_base_name}-shadow.png"))

                img = d.read_image('overlay', group, frame)
                if img is not None:
                    img.save(os.path.join(output_dir, f"{frame_base_name}-overlay.png"))

    json_path = os.path.join(foldername, f"{Path(filename).stem}.json")
    with open(json_path, "w", encoding="utf-8") as o:
        json.dump(tmp_json, o, indent=4, ensure_ascii=False)


def process_def_hdremaster(path):
    foldername = os.path.dirname(path)
    filename = os.path.basename(path)

    output_dir = os.path.join(foldername, Path(filename).stem)
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    tmp_json = {"images": [], "basepath": Path(filename).stem + "/"}

    frame_index = 0

    with deffile.open(path) as d:
        for group in d.get_groups():
            for frame in range(d.get_frame_count(group)):
                numbered_name = f"0_{frame_index}.png"
                tmp_json["images"].append({
                    "group": group,
                    "frame": frame,
                    "file": numbered_name
                })

                img = d.read_image('normal', group, frame)
                img.save(os.path.join(output_dir, numbered_name))

                img = d.read_image('shadow', group, frame)
                if img is not None:
                    img.save(os.path.join(output_dir, f"0_{frame_index}-shadow.png"))

                img = d.read_image('overlay', group, frame)
                if img is not None:
                    img.save(os.path.join(output_dir, f"0_{frame_index}-overlay.png"))

                frame_index += 1

    json_path = os.path.join(foldername, f"{Path(filename).stem}.json")
    with open(json_path, "w", encoding="utf-8") as o:
        json.dump(tmp_json, o, indent=4, ensure_ascii=False)


def main():
    args = sys.argv[1:]

    hdremaster_mode = False
    paths = []

    # Argument parsing
    if args and args[0] == "--hdremaster":
        hdremaster_mode = True
        paths = args[1:]
    else:
        paths = args

    # If no paths provided, use file dialog
    if not paths:
        Tk().withdraw()
        paths = askopenfilenames(filetypes=[("H3 def", ".def")])

    if not paths:
        print("No files selected or provided.")
        return

    # Process each file
    for path in paths:
        try:
            print(f"[INFO] Processing {path} {'(HD Remaster mode)' if hdremaster_mode else ''}")
            if hdremaster_mode:
                process_def_hdremaster(path)
            else:
                process_def_default(path)
        except Exception as e:
            ensure_logger()
            logging.error(f"Error while processing '{path}': {e}")
            messagebox.showerror("Error", f"Failed to process {path}:\n{e}")


if __name__ == "__main__":
    main()
