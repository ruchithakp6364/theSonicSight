# path_analyzer.py - Local Path Analysis for SonicSight
import numpy as np

def predict_safe_path(detections, frame_width=640):
    """
    Analyze detected objects and decide the safest movement direction.
    Returns a tuple: (direction_message, confidence)
    """

    # No detections → clear path
    if not detections:
        return "Path clear. Move straight.", 1.0

    # Divide frame horizontally into 3 zones
    left_zone = (0, frame_width // 3)
    center_zone = (frame_width // 3, 2 * frame_width // 3)
    right_zone = (2 * frame_width // 3, frame_width)

    # Initialize weighted congestion scores
    left_score = center_score = right_score = 0.0

    for d in detections:
        x1, y1, x2, y2 = d["bbox"]
        width = x2 - x1
        height = y2 - y1
        area = width * height  # proxy for closeness
        mid_x = (x1 + x2) // 2

        # Weighted impact of each object (clamped)
        weight = float(np.clip(area / 40000, 0.1, 1.0))

        if mid_x < left_zone[1]:
            left_score += weight
        elif mid_x < right_zone[0]:
            center_score += weight
        else:
            right_score += weight

    # Determine safest zone (lowest obstacle congestion)
    scores = {"left": left_score, "center": center_score, "right": right_score}
    safest = min(scores, key=scores.get)

    # Confidence inversely related to congestion
    total_score = sum(scores.values()) + 1e-6
    confidence = 1 - (scores[safest] / total_score)
    confidence = round(float(np.clip(confidence, 0.0, 1.0)), 2)

    # Convert to human-like direction message
    if safest == "left":
        msg = "Turn left."
    elif safest == "right":
        msg = "Turn right."
    else:
        msg = "Move straight."

    return msg, confidence