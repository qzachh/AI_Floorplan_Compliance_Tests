import json
import cv2
import os
import re
import numpy as np
from typing import Dict, Any, Tuple, Optional

# -------------------- text helpers --------------------
def normalize_quotes(text: str) -> str:
    """Replace curly quotes (“ ”) with straight quotes (") and remove NBSP."""
    return (text.replace("“", '"')
                .replace("”", '"')
                .replace("\u00A0", " "))

def clean_label(text: str) -> str:
    """Normalize quotes, remove ??? runs and non-ASCII control chars, trim."""
    text = normalize_quotes(text)
    text = re.sub(r"\?{2,}", "", text)  # remove ??? or longer runs
    text = text.encode("ascii", errors="ignore").decode()
    return text.strip()

# -------------------- drawing helpers --------------------
def _put_label(img, text: str, anchor_xy: Tuple[int, int], color=(0,0,255),
               font_scale=0.45, thickness=1):
    """Draw a white text bubble with the label near an anchor point."""
    h, w = img.shape[:2]
    font = cv2.FONT_HERSHEY_SIMPLEX
    text = clean_label(text)
    (tw, th), _ = cv2.getTextSize(text, font, font_scale, thickness)
    # Default place above-right of anchor
    tx = min(w - tw - 6, anchor_xy[0] + 8)
    ty = max(th + 6, anchor_xy[1] - 8)
    if ty - th - 6 < 0:  # if off-canvas, place below
        ty = min(h - 6, anchor_xy[1] + th + 12)
    # Background for readability
    cv2.rectangle(img, (tx - 4, ty - th - 4), (tx + tw + 4, ty + 4), (255,255,255), -1)
    cv2.putText(img, text, (tx, ty), font, font_scale, color, thickness, cv2.LINE_AA)

def _draw_point(img, pt, color, r=6, fill=True, thickness=2):
    cv2.circle(img, (int(pt[0]), int(pt[1])), r, color, -1 if fill else thickness)

def _draw_bbox(img, bbox, color, thickness=2):
    x1, y1, x2, y2 = map(int, bbox)
    cv2.rectangle(img, (x1, y1), (x2, y2), color, thickness)

def _draw_polyline(img, pts, color, thickness=2, closed=False):
    arr = np.array([[int(x), int(y)] for x, y in pts], dtype=np.int32)
    cv2.polylines(img, [arr], isClosed=closed, color=color, thickness=thickness)

def _centroid_from_polyline(pts) -> Tuple[int, int]:
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    return int(sum(xs)/len(xs)), int(sum(ys)/len(ys))

# -------------------- main renderer --------------------
def render_compliance_overlay(
    json_path: str,
    image_path: str,
    output_path: Optional[str] = None,
    draw_geometry: bool = True
) -> str:
    with open(json_path, "r", encoding="utf-8") as f:
        data: Dict[str, Any] = json.load(f)

    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        raise FileNotFoundError(f"Could not read image at {image_path}")

    # Colors
    GREEN = (0, 200, 0)
    ORANGE = (0, 165, 255)
    RED = (0, 0, 255)
    BLUE = (255, 0, 0)

    # Geometry (site + building outline)
    geom = data.get("geometry", {})
    if draw_geometry:
        site = geom.get("site_boundary_px")
        if site:
            _draw_polyline(img, site, GREEN, thickness=2, closed=True)
        bldg = geom.get("building_envelope_px")
        if bldg:
            _draw_polyline(img, bldg, ORANGE, thickness=2, closed=True)

    # Issues (red)
    for issue in data.get("issues", []):
        cat = issue.get("category", "unknown")
        label = issue.get("label", issue.get("id", "issue"))
        ref = issue.get("regulation_reference", "ref unknown")
        text = f"[{cat}] {label} | {ref}"

        loc = issue.get("location", {}) or {}
        anchor = None

        if loc.get("point_px"):
            _draw_point(img, loc["point_px"], RED, r=6, fill=True)
            anchor = tuple(map(int, loc["point_px"]))

        if loc.get("bbox_px"):
            _draw_bbox(img, loc["bbox_px"], RED, thickness=2)
            if anchor is None:
                x1, y1, x2, y2 = map(int, loc["bbox_px"])
                anchor = (x2, y1)

        if loc.get("polyline_px"):
            _draw_polyline(img, loc["polyline_px"], RED, thickness=2, closed=False)
            if anchor is None:
                anchor = _centroid_from_polyline(loc["polyline_px"])

        if anchor:
            _put_label(img, text, anchor, color=RED, font_scale=0.45, thickness=1)

    # Fail segments (blue)
    for seg in data.get("setback_fail_segments", []):
        pts = seg.get("points_px") or []
        anchor = None
        if pts:
            _draw_polyline(img, pts, BLUE, thickness=2, closed=False)
            anchor = _centroid_from_polyline(pts)

        # Auto label with edge_type and measurements
        bits = []
        if "edge_type" in seg: bits.append(str(seg["edge_type"]))
        if "measured_min_m" in seg: bits.append(f"{seg['measured_min_m']} m")
        if "required_m" in seg and seg["required_m"] is not None:
            bits.append(f"req {seg['required_m']} m")
        if "shortfall_m" in seg and seg["shortfall_m"] is not None:
            bits.append(f"short {seg['shortfall_m']} m")
        seg_label = clean_label(" / ".join(bits) or "setback segment")

        if anchor:
            _put_label(img, seg_label, anchor, color=BLUE, font_scale=0.45, thickness=1)

    # Output
    if output_path is None:
        root, ext = os.path.splitext(image_path)
        output_path = f"{root}_annotated{ext}"

    if not cv2.imwrite(output_path, img):
        raise IOError(f"Failed to write {output_path}")
    return output_path

# -------------------- CLI / example --------------------
if __name__ == "__main__":
    json_path = "issues.json"   # your JSON file
    image_path = "rendered_pages/page_001.jpg"             # your floor plan
    out_path = render_compliance_overlay(json_path, image_path)
    print(f"Annotated image saved to: {out_path}")