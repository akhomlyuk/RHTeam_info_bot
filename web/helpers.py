import os
from icecream import ic


def images_to_index():
    try:
        img_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static'))
        image_list = []
        file_list = os.listdir(img_dir)
        for file in file_list:
            if file.endswith(".png") or file.endswith(".jpg"):
                image_list.append(file)
        return image_list
    except Exception as e:
        ic(e)
