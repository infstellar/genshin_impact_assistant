def get_extra_params():
    # 项目根目录
    root_path = get_root_path()
    extra_data = [
        ("src\\res", "src\\res"),
        ("config", "config"),
        ("venv\\Lib\\site-packages\\Shapely.libs", "Shapely.libs"),
        ("venv\\Lib\\site-packages\\paddle", "paddle"),
        ("venv\\Lib\\site-packages\\paddleocr", "paddleocr"),
        ("venv\\Lib\\site-packages\\PIL", "PIL"),
        ("venv\\Lib\\site-packages\\pywt", "pywt"),
        ("venv\\Lib\\site-packages\\lmdb", "lmdb"),
        ("venv\\Lib\\site-packages\\shapely", "shapely"),
        ("venv\\Lib\\site-packages\\skimage", "skimage"),
        ("venv\\Lib\\site-packages\\pyclipper", "pyclipper"),
        ("venv\\Lib\\site-packages\\scipy", "scipy"),
        ("venv\\Lib\\site-packages\\imgaug", "imgaug"),
        ("venv\\Lib\\site-packages\\imageio", "imageio"),
        ("venv\\Lib\\site-packages\\attrdict", "attrdict")]
    params = []
    for item in extra_data:
        src_path = os.path.join(root_path, item[0])
        params.extend(["--add-data", f"{src_path};{item[1]}"])
    return params


import paddleocr


print(paddleocr)