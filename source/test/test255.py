from source.util import *
from source.interaction.interaction_core import itt
print("go")
for i in []:
    img = cv2.imread(i)
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Draw ellipse on mask
    mask = np.zeros_like(gray)
    cv2.ellipse(mask, (960, 540), (510+30, 430+30), 0, 0, 360, 255, -1)
    cv2.ellipse(mask, (960, 540), (510-50, 430-50), 0, 0, 360, 0, -1)

    # Apply mask to image
    result = cv2.bitwise_and(img, img, mask=mask)

    # Display result
    cv2.imshow(i, result)
cv2.waitKey(0)
cv2.destroyAllWindows()
