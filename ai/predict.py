from ultralytics import YOLO
import cv2
import os
import math

# Config
MODEL_PATH = "D://PulleyDetector//ai//runs//detect//yolov11m-custom//weights//best.pt"
IMAGE_PATH = "D://PulleyDetector//ai//2.jpg" 
# IMAGE_PATH = "D://yolo_model_trian//1.jpg"  # change to your image path
MM_PER_PIXEL = 1.0  # set your real-world scale (millimeters per pixel)
# Thermal compensation defaults (total first->third distance)
BASE_TEMPERATURE_C = 35.0
STANDARD_TOTAL_DISTANCE_MM = 1300.0  # reference "standard" used for loss computation (1300 - total)
TEMPERATURE_SENSITIVITY_MM_PER_C = 0.5  # used only if chart lookup is unavailable
CURRENT_TEMPERATURE_C = 35.0  # update this with the measured temperature

# Chart-based values for total distance X (1->3) vs temperature (°C).
# Fill this with rows from your chart (Temp row → corresponding total X in mm).
# If exact temperature isn't present, we will interpolate between surrounding keys.
# Example starter data (edit/extend these according to your table):
TEMP_TO_TOTAL_DISTANCE_MM = {
    10.0: 1385.0,
    15.0: 1368.0,
    20.0: 1351.0,
    21.0: 1348.0,
    22.0: 1344.0,
    23.0: 1341.0,
    24.0: 1337.0,
    25.0: 1334.0,
    26.0: 1331.0,
    27.0: 1327.0,
    28.0: 1324.0,
    29.0: 1320.0,
    30.0: 1317.0,
    31.0: 1314.0,
    32.0: 1310.0,
    33.0: 1307.0,
    34.0: 1303.0,
    35.0: 1300.0,
    36.0: 1297.0,
    37.0: 1293.0,
    38.0: 1290.0,
    39.0: 1286.0,
    40.0: 1283.0,
    41.0: 1280.0,
    42.0: 1276.0,
    43.0: 1273.0,
    44.0: 1269.0,
    45.0: 1266.0,
    50.0: 1249.0,
}

# Ratio assumptions for a 3:1 pulley layout (first->second, second->third)
DISTANCE_RATIO_12 = 0.75
DISTANCE_RATIO_23 = 0.25
# NUMBERING_SIDE = "left"  # choose "left" (default) or "right" to start numbering from that side


model = YOLO(MODEL_PATH)

results = model.predict(source=IMAGE_PATH, save=True, verbose=False)
if not results:
    raise RuntimeError("No results returned by the model.")

result = results[0]
if result.boxes is None or len(result.boxes) == 0:
    raise RuntimeError("No detections found in the image.")

names = result.names if hasattr(result, "names") else model.names
boxes = result.boxes
cls_indices = boxes.cls.cpu().numpy().astype(int)
xyxy = boxes.xyxy.cpu().numpy()

# Collect pulley centers
pulley_points = []
for i, c in enumerate(cls_indices):
    label = names.get(int(c), str(c)) if isinstance(names, dict) else names[int(c)]
    if str(label).lower() == "pulley":
        x1, y1, x2, y2 = xyxy[i]
        cx = (x1 + x2) / 2.0
        cy = (y1 + y2) / 2.0
        pulley_points.append((cx, cy))

if len(pulley_points) < 2:
    raise RuntimeError("Found fewer than 2 pulleys. Need at least 2 to compute distance.")

# Sort left-to-right to define first, second, third
pulley_points.sort(key=lambda p: p[0])
p1 = pulley_points[0] if len(pulley_points) >= 1 else None
p2 = pulley_points[1] if len(pulley_points) >= 2 else None
p3 = pulley_points[2] if len(pulley_points) >= 3 else None

# Load image for drawing
img = cv2.imread(IMAGE_PATH)
if img is None:
    raise RuntimeError(f"Failed to load image: {IMAGE_PATH}")

# Draw points
for (cx, cy) in pulley_points:
    cv2.circle(img, (int(cx), int(cy)), 6, (0, 255, 0), -1)
# Draw pulley indices (1, 2, 3) next to centers
for idx, (cx, cy) in enumerate(pulley_points, start=1):
    cv2.putText(
        img,
        f"{idx}",
        (int(cx) + 8, int(cy) - 8),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (0, 255, 255),
        2,
        cv2.LINE_AA
    )

def pixel_distance(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

def _chart_total_distance(temp_c):
    """
    Return chart-based total distance X for temperature (with linear interpolation).
    If the chart has no data, return None.
    """
    if not TEMP_TO_TOTAL_DISTANCE_MM:
        return None
    # Exact hit
    if temp_c in TEMP_TO_TOTAL_DISTANCE_MM:
        return float(TEMP_TO_TOTAL_DISTANCE_MM[temp_c])
    # Find neighbors for interpolation
    keys = sorted(TEMP_TO_TOTAL_DISTANCE_MM.keys())
    if temp_c <= keys[0]:
        return float(TEMP_TO_TOTAL_DISTANCE_MM[keys[0]])
    if temp_c >= keys[-1]:
        return float(TEMP_TO_TOTAL_DISTANCE_MM[keys[-1]])
    lower = None
    upper = None
    for k in keys:
        if k < temp_c:
            lower = k
        elif k > temp_c:
            upper = k
            break
    if lower is None or upper is None:
        return None
    x0 = lower
    y0 = float(TEMP_TO_TOTAL_DISTANCE_MM[lower])
    x1 = upper
    y1 = float(TEMP_TO_TOTAL_DISTANCE_MM[upper])
    ratio = (temp_c - x0) / (x1 - x0)
    return y0 + ratio * (y1 - y0)

def expected_total_distance_for_temperature(temp_c):
    """
    Compute expected total pulley distance (1->3) in mm for the given temperature.
    Priority: use chart values (with interpolation). If unavailable, fall back to linear model.
    """
    chart_value = _chart_total_distance(temp_c)
    if chart_value is not None:
        return chart_value
    delta_t = temp_c - BASE_TEMPERATURE_C
    return STANDARD_TOTAL_DISTANCE_MM - TEMPERATURE_SENSITIVITY_MM_PER_C * delta_t

def temperature_from_total_distance(distance_mm):
    """
    Estimate temperature (°C) from a measured total pulley distance 1->3.
    """
    delta_d = STANDARD_TOTAL_DISTANCE_MM - distance_mm
    return BASE_TEMPERATURE_C + (delta_d / TEMPERATURE_SENSITIVITY_MM_PER_C)

def split_total_distance(distance_mm):
    """
    Split total 1->3 distance into 1->2 and 2->3 spans using configured ratios.
    """
    return (
        distance_mm * DISTANCE_RATIO_12,
        distance_mm * DISTANCE_RATIO_23
    )

dist12_mm = None
dist23_mm = None

# Compute and draw 1->2
if p1 is not None and p2 is not None:
    d_px = pixel_distance(p1, p2)
    dist12_mm = d_px * MM_PER_PIXEL
    cv2.line(img, (int(p1[0]), int(p1[1])), (int(p2[0]), int(p2[1])), (0, 0, 255), 2)
    mid12 = (int((p1[0] + p2[0]) / 2), int((p1[1] + p2[1]) / 2))
    cv2.putText(img, f"{dist12_mm:.2f} mm", mid12, cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)

# Compute and draw 2->3
total_distance_mm = None

if p2 is not None and p3 is not None:
    d_px = pixel_distance(p2, p3)
    dist23_mm = d_px * MM_PER_PIXEL
    cv2.line(img, (int(p2[0]), int(p2[1])), (int(p3[0]), int(p3[1])), (255, 0, 0), 2)
    mid23 = (int((p2[0] + p3[0]) / 2), int((p2[1] + p3[1]) / 2))
    cv2.putText(img, f"{dist23_mm:.2f} mm", mid23, cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2, cv2.LINE_AA)

if dist12_mm is not None and dist23_mm is not None:
    total_distance_mm = dist12_mm + dist23_mm

if total_distance_mm is not None and TEMPERATURE_SENSITIVITY_MM_PER_C > 0 and p1 is not None and p3 is not None:
    expected_total = expected_total_distance_for_temperature(CURRENT_TEMPERATURE_C)
    expected_dist12, expected_dist23 = split_total_distance(expected_total)
    estimated_temp = temperature_from_total_distance(total_distance_mm)
    loss_mm = expected_total - total_distance_mm
    info_lines = [
        f"Pulley 1->Pulley 2: {dist12_mm:.3f} mm",
        f"Pulley 2->Pulley 3: {dist23_mm:.3f} mm",
        f"Total distance (1->3): {total_distance_mm:.3f} mm",
        f"Expected @ {CURRENT_TEMPERATURE_C:.1f} °C (1->3): {expected_total:.3f} mm",
        f"Expected 1->2: {expected_dist23:.3f} mm | 2->3: {expected_dist12:.3f} mm",
        f"Loss vs expected:{CURRENT_TEMPERATURE_C:.1f} °C: {expected_total:.3f} mm - {total_distance_mm:.3f} mm = {loss_mm:.3f} mm",
        # f"Estimated temperature: {estimated_temp:.2f} C"
    ]
    text_y = int(min(p1[1], p3[1]) - 10)
    for line in info_lines:
        cv2.putText(
            img,
            line,
            (int((p1[0] + p3[0]) / 2 - 160), max(text_y, 30)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 0, 0),
            2,
            cv2.LINE_AA
        )
        text_y -= 25

# Save annotated image next to source
root, ext = os.path.splitext(IMAGE_PATH)
out_path = f"{root}_annotated{ext}"
cv2.imwrite(out_path, img)

# Print distances
if dist12_mm is not None:
    print(f"Distance first->second pulley: {dist12_mm:.3f} mm (scale {MM_PER_PIXEL} mm/px)")
if dist23_mm is not None:
    print(f"Distance second->third pulley: {dist23_mm:.3f} mm (scale {MM_PER_PIXEL} mm/px)")
if total_distance_mm is not None and TEMPERATURE_SENSITIVITY_MM_PER_C > 0:
    expected_total = expected_total_distance_for_temperature(CURRENT_TEMPERATURE_C)
    expected_dist12, expected_dist23 = split_total_distance(expected_total)
    estimated_temp = temperature_from_total_distance(total_distance_mm)
    loss_mm = expected_total - total_distance_mm
    print(f"Expected total distance (1->3) at {CURRENT_TEMPERATURE_C:.1f} °C: {expected_total:.3f} mm")
    print(f"Expected split: 1->2 = {expected_dist12:.3f} mm, 2->3 = {expected_dist23:.3f} mm")
    print(f"Measured total distance (1->3): {total_distance_mm:.3f} mm")
    print(f"Loss vs expected:{CURRENT_TEMPERATURE_C:.1f} °C: {expected_total:.3f} mm - {total_distance_mm:.3f} mm = {loss_mm:.3f} mm")
    # print(f"Estimated temperature from measured total: {estimated_temp:.3f} °C")
if len(pulley_points) < 3:
    print("Only two pulleys detected; third-to-second distance not computed.")
print(f"Annotated image saved to: {out_path}")
