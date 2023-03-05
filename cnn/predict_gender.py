import keras
import os
import numpy as np
from PIL import Image
from numpy import asarray

from django.conf import settings


IMG_SIZE = settings.IMG_SIZE
BASE_DIR = settings.BASE_DIR


def predict(title: str) -> int:
    """Принимает имя загруженной фотографии и возвращает: 1 - на фото мужчина, 0 - женщина"""

    model_path = os.path.join(BASE_DIR, 'cnn/model/gender_model')
    model = keras.models.load_model(model_path)
    image = np.array( [image_to_arr(title),] )
    prediction = model.predict(image)

    return 1 if prediction[0][1] > prediction[0][0] else 0


def image_to_arr(title: str):
    """Преобразует фотографию в массив"""

    image_path = os.path.join(settings.BASE_DIR, f'media/faces/{title}.jpg')
    img = Image.open(image_path).resize((IMG_SIZE, IMG_SIZE)).convert('L')

    return asarray(img)
