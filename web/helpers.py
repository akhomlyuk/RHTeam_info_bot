import os
from icecream import ic


def images_to_index():
    try:
        img_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static'))
        image_list = []
        file_list = sorted(os.scandir(img_dir), key=lambda f: os.path.getmtime(f.path), reverse=True)

        for file in file_list:
            if file.name.endswith(".png") or file.name.endswith(".jpg"):
                image_list.append(file.name)
        return image_list
    except Exception as e:
        ic(e)
