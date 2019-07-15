# /src/views/VideoView

from flask import request, json, Response, Blueprint
from ..models.videoModel import VideoModel, VideoSchema
import pybase64
from pathlib import Path
from datetime import datetime
from ..detection.predict import predictionPicture

video_api = Blueprint('video', __name__)
video_schema = VideoSchema()
video_folder = Path("C:/Users/Mega Evia Maharani/PycharmProjects/skripsong/src/detection")


@video_api.route('/input', methods=['POST'])
def create():
    req_data = request.get_json()
    predict = req_data.get ("inputan")
    now = datetime.now()
    tanggal = str(now.strftime("%m%d%Y%H%M%S"))

    # simpan video ke folder
    video = pybase64.b64decode(predict)
    path_simpan = str(tanggal + ".jpg")
    video_tanggal = open(video_folder / path_simpan, "wb")
    video_simpan = open(video_folder / "photo.jpg", "wb")
    video_tanggal.write(video)
    video_simpan.write(video)
    video_tanggal.close()
    video_simpan.close()
    hasil_prediksi, golongan = predictionPicture.predict()
    print("golongan", golongan)
    print("hasil_prediksi", hasil_prediksi)
    input = {"golongan": golongan, "nama_video": path_simpan, "tanggal": tanggal}

    data, error = video_schema.load(input)

    if error :
        return custom_response(error, 400)

    video_save = VideoModel(data)
    video_save.save()

    #ser_data = video_schema.dump(video_save).data
    return custom_response({"Golongan": golongan, "Hasil_prediksi": hasil_prediksi}, 200)
    #return custom_response({"Data di database :": ser_data, "Hasil Prediksi :": hasil_prediksi, "Golongan: ": golongan},200)

@video_api.route('/get/golongan', methods=['GET'])
def get_golongan():
    golongan1 = VideoModel.filter_gol1()
    golongan2 = VideoModel.filter_gol2()
    golongan3 = VideoModel.filter_gol3()
    return custom_response({"Golongan_1":golongan1, "Golongan_2":golongan2, "Golongan_3":golongan3}, 200)

def custom_response(res, status_code):
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )