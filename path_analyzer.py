def predict_safe_path(detections):
    """
    Simple logic: choose direction with fewer obstacles.
    """
    left = right = 0
    for d in detections:
        x1, _, x2, _ = d["bbox"]
        if (x1 + x2) / 2 < 320:
            left += 1
        else:
            right += 1
    if left < right:
        return "Move left"
    elif right < left:
        return "Move right"
    return "Proceed straight"
