from datetime import datetime
from api.models.db import db

class Character(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    role = db.Column(db.String(100))
    description = db.Column(db.String(250))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'))

    def __repr__(self):
      return f"Character('{self.id}', '{self.name}'"

    def serialize(self):
      character = {c.name: getattr(self, c.name) for c in self.__table__.columns}
      return character