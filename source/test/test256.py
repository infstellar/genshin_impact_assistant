import numpy as np
def convert_coordinates(x, y):
    new_x = x - 720
    new_y = 540 - y
    return new_x, new_y

def ellipse_equation(x1, y1, x2, y2):
    # Center of the ellipse
    x0 = (x1 + x2) / 2
    y0 = (y1 + y2) / 2

    # Distance between the two points
    d = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    # Semi-major and semi-minor axes
    a = d / 2
    b = np.sqrt(a ** 2 - ((y2 - y1) / (x2 - x1)) ** 2 * a ** 2)

    # Angle of rotation
    theta = np.arctan2(y2 - y1, x2 - x1)

    # Standard equation of the ellipse
    return f"((x - {x0}) * np.cos({theta}) + (y - {y0}) * np.sin({theta})) ** 2 / {a ** 2} + ((x - {x0}) * np.sin({theta}) - (y - {y0}) * np.cos({theta})) ** 2 / {b ** 2} = 1"
# Welcome to Cursor

def convert_to_opencv_params(x1, y1, x2, y2):
    # Center of the ellipse
    x0 = (x1 + x2) / 2
    y0 = (y1 + y2) / 2

    # Distance between the two points
    d = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    # Semi-major and semi-minor axes
    a = d / 2
    b = np.sqrt(a ** 2 - ((y2 - y1) / (x2 - x1)) ** 2 * a ** 2)

    # Angle of rotation
    theta = np.arctan2(y2 - y1, x2 - x1)

    # Convert angle to degrees
    angle_degrees = np.degrees(theta)

    # Return parameters for OpenCV ellipse function
    return (int(x0), int(y0)), (int(a), int(b)), angle_degrees, 0, 360, (0, 0, 255), 2


x1,y1 = convert_coordinates(455,483)
x2,y2 = convert_coordinates(1193,893)
print(convert_to_opencv_params(x1,y1,x2,y2))