from PIL import Image
from math import floor
from db_utils import DB_FILE  # keep dependency minimal
import os
from typing import Tuple

# Default A4 size in mm
A4_MM = (210, 297)
DEFAULT_DPI = 203

def mm_to_px(mm, dpi=DEFAULT_DPI):
    return int((float(mm) / 25.4) * dpi)

def create_a4_from_label(label_img: Image.Image, margin_mm: float = 10,
                         rows: int = 1, cols: int = 1, dpi: int = DEFAULT_DPI) -> Image.Image:
    """
    Place one or multiple label images onto an A4 canvas with margins.
    - margin_mm: outer margin around the page (in mm)
    - rows, cols: how many labels vertically/horizontally to tile
    The label image will be scaled uniformly to fit the cell size.
    """
    a4_w_px = mm_to_px(A4_MM[0], dpi=dpi)
    a4_h_px = mm_to_px(A4_MM[1], dpi=dpi)
    margin_px = mm_to_px(margin_mm, dpi=dpi)
    usable_w = a4_w_px - 2 * margin_px
    usable_h = a4_h_px - 2 * margin_px
    if rows <= 0 or cols <= 0:
        raise ValueError("rows and cols must be >= 1")
    cell_w = usable_w // cols
    cell_h = usable_h // rows

    a4 = Image.new("RGB", (a4_w_px, a4_h_px), "white")

    # For each grid cell, place a centered scaled version of label_img
    lw, lh = label_img.size
    for r in range(rows):
        for c in range(cols):
            max_w = cell_w
            max_h = cell_h
            scale = min(max_w / lw, max_h / lh, 1.0)
            new_w = max(1, int(lw * scale)); new_h = max(1, int(lh * scale))
            label_resized = label_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
            # compute position within the page
            x0 = margin_px + c * cell_w + (cell_w - new_w) // 2
            y0 = margin_px + r * cell_h + (cell_h - new_h) // 2
            a4.paste(label_resized, (x0, y0))
    return a4