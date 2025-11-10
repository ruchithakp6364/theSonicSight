_prev_sizes = {}

def calculate_ttc(label, bbox, fps=30):
    global _prev_sizes
    (x1, y1, x2, y2) = bbox
    area = (x2 - x1) * (y2 - y1)
    ttc = None

    if label in _prev_sizes:
        prev_area = _prev_sizes[label]
        if prev_area > 0 and area > prev_area:
            growth = (area - prev_area) / prev_area
            if growth > 0:
                ttc = round(1 / (growth * fps), 2)
    _prev_sizes[label] = area
    return ttc
