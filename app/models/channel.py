from __future__ import annotations

from sqlalchemy.sql import expression

from app.models.db import TimedBaseModel, db


class Channel(TimedBaseModel):
    __tablename__ = "channels"

    id = db.Column(db.Integer, primary_key=True, index=True, unique=True)
    chat_id = db.Column(db.String)
    name = db.Column(db.String)
    publications_counter_total = db.Column(db.Integer, default=0)
    publications_counter_day = db.Column(db.Integer, default=0)
    last_publication_datetime = db.Column(db.DateTime, server_default=db.func.now())
    count_of_publications = db.Column(db.Integer, default=1)
    start_time_publications = db.Column(db.Time)
    end_time_publications = db.Column(db.Time)
    is_enable = db.Column(db.Boolean, server_default=expression.false())
