import keras
from keras.layers import Dense, Conv2D, Flatten, MaxPooling2D
from PIL import Image
from numpy import asarray
import os
import numpy as np
import random


IMG_SIZE = 200


def get_train_data(begin: int = 0, end: int = 0):
    """Возвращает данные для тренировки модели"""
    
    print(f'Подготовка данных для обучения\nДиапазон {begin}:{end}')
    gender_path = f'../dataset/Male'
    x_train = []    # входные данные
    y_train = []    # выходные

    # получаем список файлов из датасета
    if end != 0:
        files = os.listdir(gender_path)[begin:end]
    else:
        files = os.listdir(gender_path)[begin:]
    for file in files:
        # открываем фото, изменяем размер и переводим в серый цвет
        img = Image.open(f'{gender_path}/{file}').resize((IMG_SIZE, IMG_SIZE)).convert('L')
        x_train.append(asarray(img))
        y_train.append(1)	# 1 - класс мужчин
    print(f'Подгтовлено {len(x_train)} данных')
    
    gender_path = f'../dataset/Female'
    if end != 0:
        files = os.listdir(gender_path)[begin:end]
    else:
        files = os.listdir(gender_path)[begin:]
    for file in files:
        img = Image.open(f'{gender_path}/{file}').resize((IMG_SIZE, IMG_SIZE)).convert('L')
        x_train.append(asarray(img))
        y_train.append(0)	# 0 - класс женщин
    print(f'Подгтовлено {len(x_train)} данных')
    
    print('Перемешиваем данные')
    new_x_train = []
    new_y_train = []
    used = []
    while len(used) != len(x_train):
        k = random.randint(0, len(x_train) - 1)
        if k not in used:
            used.append(k)
            new_x_train.append(x_train[k])
            new_y_train.append(y_train[k])
    print(f'Всего подготвленно данных: {len(new_x_train)}')
    
    return (new_x_train, new_y_train)


def create_model():
    """Создает модель сверточной нейросети"""

    model = keras.Sequential([
        Conv2D(32, (3, 3), padding='same', activation='relu', input_shape=(IMG_SIZE, IMG_SIZE, 1)),
        MaxPooling2D((2, 2), strides=2),
        Conv2D(64, (3, 3), padding='same', activation='relu'),
        MaxPooling2D((2, 2), strides=2),
        Conv2D(128, (3, 3), padding='same', activation='relu'),
        MaxPooling2D((2, 2), strides=2),
        Conv2D(256, (3, 3), padding='same', activation='relu'),
        MaxPooling2D((2, 2), strides=2),
        Flatten(),
        Dense(128, activation='relu'),
        Dense(2,  activation='sigmoid')
    ])

    model.compile(optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])
    model.save('model/gender_model', save_format='h5')


def train(begin: int = 0, end: int = 0, epochs: int = 3):
    """Обучает модель"""

    model_path = 'model/gender_model'
    model = keras.models.load_model(model_path)

    (x_train, y_train) = get_train_data(begin=begin, end=end)
    y_train_cat = keras.utils.to_categorical(y_train, 2)
    x_train = np.expand_dims(x_train, axis=3)

    model.fit(x_train, y_train_cat, batch_size=32, epochs=epochs, validation_split=0.1)
    model.save('model/gender_model', save_format='h5')


if __name__ == '__main__':
    train(begin=5000, end=5100)
