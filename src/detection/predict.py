import cv2
from pathlib import Path
from keras.models import load_model
from keras import backend as K
import numpy as np
from keras.preprocessing.image import img_to_array, load_img

path = Path("C:/Users/Mega Evia Maharani/PycharmProjects/skripsong/src/detection")

class predictionPicture():
    @staticmethod
    def predict():
        K.clear_session()
        path_model = path / "modelgabungan.h5"
        model = load_model(str (path_model))
        img_width, img_heigt = 70, 70

        image_path = path / "photo.jpg"
        image_file = str (image_path)
        x = load_img(image_file, target_size=(img_width, img_heigt))
        x = img_to_array(x)
        x = np.expand_dims(x, axis=0)
        array = model.predict(x)
        result = array[0]

        answer = np.argmax(result)
        if answer == 0:
            hasil_prediksi = "bus"
            golongan = "II"

        elif answer == 1:
            hasil_prediksi = "pribadi"
            golongan = "I"

        elif answer == 2:
            hasil_prediksi = "truck"
            golongan = "III"

        K.clear_session()

        return hasil_prediksi, golongan