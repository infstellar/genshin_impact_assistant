from source.device.alas.utils import *


def create_circular_mask(h, w, center=None, radius=None):
    # https://stackoverflow.com/questions/44865023/how-can-i-create-a-circular-mask-for-a-numpy-array
    if center is None:  # use the middle of the image
        center = (int(w / 2), int(h / 2))
    if radius is None:  # use the smallest distance between the center and image walls
        radius = min(center[0], center[1], w - center[0], h - center[1])

    y, x = np.ogrid[:h, :w]
    dist_from_center = np.sqrt((x - center[0]) ** 2 + (y - center[1]) ** 2)

    mask = dist_from_center <= radius
    return mask


def rotate_bound(image, angle):
    """
    Rotate an image with outbound

    https://blog.csdn.net/qq_37674858/article/details/80708393

    Args:
        image (np.ndarray):
        angle (int, float):

    Returns:
        np.ndarray:
    """
    # grab the dimensions of the image and then determine the
    # center
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)

    # grab the rotation matrix (applying the negative of the
    # angle to rotate clockwise), then grab the sine and cosine
    # (i.e., the rotation components of the matrix)
    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])

    # compute the new bounding dimensions of the image
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))

    # adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY

    # perform the actual rotation and return the image
    return cv2.warpAffine(image, M, (nW, nH))


def cubic_find_maximum(image, precision=0.05):
    """
    Using CUBIC resize algorithm to fit a curved surface, find the maximum value and location.

    Args:
        image:
        precision:

    Returns:
        float: Maximum value on curved surface
        np.ndarray[float, float]: Location of maximum value
    """
    image = cv2.resize(image, None, fx=1 / precision, fy=1 / precision, interpolation=cv2.INTER_CUBIC)
    _, sim, _, loca = cv2.minMaxLoc(image)
    loca = np.array(loca, dtype=np.float64) * precision
    return sim, loca
