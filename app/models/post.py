from __future__ import annotations

from sqlalchemy.sql import expression

from app.models.db import TimedBaseModel, db


class Post(TimedBaseModel):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, index=True, unique=True)
    donor_id = db.Column(db.Integer, db.ForeignKey('donors.id'))
    channel_id = db.Column(db.Integer, db.ForeignKey('channels.id'))
    title = db.Column(db.String)
    photo = db.Column(db.ARRAY(db.String))
    video = db.Column(db.ARRAY(db.String))
    type = db.Column(db.String, default=0)
    publication_date = db.Column(db.DateTime)
    is_enable = db.Column(db.Boolean, server_default=expression.false())
