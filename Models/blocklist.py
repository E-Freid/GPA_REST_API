from db import db


class BlockListModel(db.Model):
    __tablename__ = "blocklist"

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(), unique=True, nullable=False)
    exp = db.Column(db.DateTime, nullable=False)
