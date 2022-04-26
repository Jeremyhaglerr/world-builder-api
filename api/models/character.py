from datetime import datetime
from api.models.db import db

class Association(db.Model):
    __tablename__ = 'associations'
    id = db.Column(db.Integer, primary_key=True)
    story_id = db.Column(db.Integer, db.ForeignKey('story.id', ondelete='cascade'))
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id', ondelete='cascade'))

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