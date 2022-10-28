def extract_white_letters(image, threshold=128):
    """Set letter color to black, set background color to white.
    This function will discourage color pixels (Non-gray pixels)
    Args:
        image: Shape (height, width, channel)
        threshold (int):
    Returns:
        np.ndarray: Shape (height, width)
    """
    r, g, b = cv2.split(cv2.subtract((255, 255, 255, 0), image))
    minimum = cv2.min(cv2.min(r, g), b)
    maximum = cv2.max(cv2.max(r, g), b)
    return cv2.multiply(cv2.add(maximum, cv2.subtract(maximum, minimum)), 255.0 / threshold)


def extract_letters(image, letter=(255, 255, 255), threshold=128):
    """Set letter color to black, set background color to white.
    Args:
        image: Shape (height, width, channel)
        letter (tuple): Letter RGB.
        threshold (int):
    Returns:
        np.ndarray: Shape (height, width)
    """
    r, g, b = cv2.split(cv2.subtract(image, (*letter, 0)))
    positive = cv2.max(cv2.max(r, g), b)
    r, g, b = cv2.split(cv2.subtract((*letter, 0), image))
    negative = cv2.max(cv2.max(r, g), b)
    return cv2.multiply(cv2.add(positive, negative), 255.0 / threshold)
