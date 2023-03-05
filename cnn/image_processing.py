import os
import cv2
import random
import math
import numpy as np
from PIL import Image

from django.conf import settings

from user.models import UserImage


BASE_DIR = settings.BASE_DIR


def generate_title() -> str:
    """Генерирует уникальный title"""

    while True:
        title = ''.join([str(random.randint(0, 9)) for _ in range(10)])
        if not UserImage.objects.filter(title=title).exists():
            break
    return title


def get_face(title: str) -> dict:
    """Выделяет лицо на фотографии из быза и сохраняет"""

    user_img = UserImage.objects.get(title=title)
    image_path = os.path.join(BASE_DIR, f'media/{user_img.image}')

    prototxt_path = os.path.join(BASE_DIR, "cnn/weights/deploy.prototxt.txt")
    model_path = os.path.join(BASE_DIR, "cnn/weights/res10_300x300_ssd_iter_140000_fp16.caffemodel")

    model = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)
    image = cv2.imread(image_path)
    h, w = image.shape[:2]

    blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300), (104.0, 177.0, 123.0))

    model.setInput(blob)
    output = np.squeeze(model.forward())

    pr = 0.15
    max_confidence = output[0, 2]
    
    if max_confidence > 0.5:
        box = output[0, 3:7] * np.array([w, h, w, h])
        start_x, start_y, end_x, end_y = box.astype(np.int)
        width = end_x - start_x
        height = end_y - start_y
        diff = abs(height - width)
        if height > width:
            diff = height - width
            if diff % 2 == 0:
                start_x -= diff//2
                end_x += diff//2
            else:
                start_x -= math.floor(diff//2)
                end_x += (diff//2) + 1
        else:
            if diff % 2 == 0:
                start_y -= diff//2
                end_y += diff//2
            else:
                start_y -= math.floor(diff//2)
                end_y += (diff//2) + 1
        start_x += round(width*pr)
        end_x -= round(width*pr)
        start_y += round(width*pr)
        end_y -= round(width*pr)

        image_pillow = Image.open(image_path)
        new_path = f'media/faces/{title}.jpg'
        image_pillow.crop((start_x, start_y, end_x, end_y)).save(os.path.join(BASE_DIR, new_path))

        return {'result': True, 'img_path': new_path}
    
    user_img.delete()
    os.remove(image_path)
    return {'result': False}
