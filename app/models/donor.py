from __future__ import annotations

from sqlalchemy.sql import expression

from app.models.db import TimedBaseModel, db


class Donor(TimedBaseModel):
    __tablename__ = "donors"

    id = db.Column(db.Integer, primary_key=True, index=True, unique=True)
    type = db.Column(db.String)
    name = db.Column(db.String)
    link = db.Column(db.String)
    parsing_rate = db.Column(db.Integer, default=0)
    is_enable = db.Column(db.Boolean, server_default=expression.false())
    channel_id = db.Column(db.Integer, db.ForeignKey('channels.id'))
