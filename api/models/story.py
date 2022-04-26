from datetime import datetime
from api.models.db import db

class Story(db.Model):
    __tablename__ = 'story'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    world = db.Column(db.String(100))
    content = db.Column(db.String(1000))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'))

    # Relationships:
    characters = db.relationship("Character", secondary="associations")

    def __repr__(self):
      return f"Story('{self.id}', '{self.name}'"

    def serialize(self):
      story = {c.name: getattr(self, c.name) for c in self.__table__.columns}
      characters = [character.serialize() for character in self.characters]
      story['characters'] = characters
      return story