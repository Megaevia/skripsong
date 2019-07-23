from marshmallow import fields, Schema
import datetime
from . import db

class VideoModel (db.Model):
    __tablename__ = 'Video'

    id = db.Column(db.Integer, primary_key=True)
    golongan = db.Column(db.String(5), nullable=True)
    nama_video = db.Column(db.String(128), nullable=True)
    tanggal = db.Column(db.String(128), nullable=True)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    def __init__(self, data):
        self.id = data.get ('id')
        self.golongan = data.get ('golongan')
        self.nama_video = data.get ('nama_video')
        self.tanggal = data.get ('tanggal')
        self.created_at = datetime.datetime.now()
        self.modified_at = datetime.datetime.now()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        self.modified_at = datetime.datetime.utcnow()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_videos():
        return VideoModel.query.all()
    
    @staticmethod
    def filter_gol1():
        return  VideoModel.query.filter(VideoModel.golongan == "I").count()

    @staticmethod
    def filter_gol2():
        return VideoModel.query.filter(VideoModel.golongan == "II").count()

    @staticmethod
    def filter_gol3():
        return VideoModel.query.filter(VideoModel.golongan == "III").count()

    @staticmethod
    def get_one_video(id):
        return VideoModel.query.get(id)

    def __repr(self):
        return '<id {}>'.format(self.id)

class VideoSchema(Schema):
    id = fields.Int(dump_only=True)
    golongan = fields.Str(required=True)
    nama_video = fields.Str(required=True)
    tanggal = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
