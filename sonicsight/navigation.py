import time
from sonicsight.path_analyzer import predict_safe_path

# Simulated coordinates
current_position = [0, 0]
destination = [0, 10]  # demo goal: 10 units straight ahead
speed = 0.2  # simulated speed per frame

def calculate_ttc(label, bbox, fps=30):
    """
    Estimate Time-To-Collision (TTC) based on object size in the frame.
    Larger bounding box => closer object.
    """
    try:
        x1, y1, x2, y2 = bbox
        object_size = (x2 - x1) * (y2 - y1)
        # Simple heuristic: larger size → smaller TTC
        ttc = max(0.5, min(5.0, 50000 / (object_size + 1)))
        return round(ttc, 2)
    except Exception:
        return None


def update_navigation_state(detections, frame_width=640):
    """
    Move toward destination while avoiding obstacles intelligently.
    Combines object detections and safe path analysis.
    """
    global current_position
    nav_message = ""

    # Get direction suggestion and confidence from path analyzer
    path_message, confidence = predict_safe_path(detections, frame_width)

    # Adjust speed based on scene congestion (confidence)
    if confidence > 0.7:
        current_position[1] += speed
        nav_message = f"{path_message} Moving at normal speed."
    elif confidence > 0.4:
        current_position[1] += speed * 0.5
        nav_message = f"{path_message} Area congested, slowing down."
    else:
        nav_message = f"{path_message} Too crowded. Holding position."

    # Apply lateral movement (left/right)
    if "left" in path_message.lower():
        current_position[0] -= 0.2
    elif "right" in path_message.lower():
        current_position[0] += 0.2

    # Compute distance to destination
    distance_to_goal = ((destination[0] - current_position[0])**2 +
                        (destination[1] - current_position[1])**2) ** 0.5

    if distance_to_goal < 0.5:
        nav_message = "Destination reached."

    return nav_message, distance_to_goal