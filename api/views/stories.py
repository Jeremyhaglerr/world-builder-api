from flask import Blueprint, jsonify, request
from api.middleware import login_required, read_token

from api.models.db import db
from api.models.story import Story
from api.models.character import Character
from api.models.character import Association

stories = Blueprint('stories', 'stories')

@stories.route('/', methods=["POST"])
@login_required
def create():
  data = request.get_json()
  profile = read_token(request)
  data["profile_id"] = profile["id"]
  story = Story(**data)
  db.session.add(story)
  db.session.commit()
  return jsonify(story.serialize()), 201

@stories.route('/', methods=["GET"])
def index():
  stories = Story.query.all()
  return jsonify([story.serialize() for story in stories]), 200

@stories.route('/<id>', methods=["GET"])
def show(id):
  story = Story.query.filter_by(id=id).first()
  story_data = story.serialize()
  characters = Character.query.filter(Character.id.notin_([character.id for character in story.characters])).all()
  characters=[character.serialize() for character in characters]
  return jsonify(story=story_data, available_characters=characters), 200

@stories.route('/<id>', methods=["PUT"]) 
@login_required
def update(id):
  data = request.get_json()
  profile = read_token(request)
  story = Story.query.filter_by(id=id).first()

  if story.profile_id != profile["id"]:
    return 'Forbidden', 403

  for key in data:
    setattr(story, key, data[key])

  db.session.commit()
  return jsonify(story.serialize()), 200

@stories.route('/<id>', methods=["DELETE"]) 
@login_required
def delete(id):
  profile = read_token(request)
  story = Story.query.filter_by(id=id).first()

  if story.profile_id != profile["id"]:
    return 'Forbidden', 403

  db.session.delete(story)
  db.session.commit()
  return jsonify(message="Success"), 200

@stories.route('/<story_id>/characters/<character_id>', methods=["LINK"])
@login_required
def assoc_character(story_id, character_id):
  data = { "story_id": story_id, "character_id": character_id }

  profile = read_token(request)
  story = Story.query.filter_by(id=story_id).first()
  
  if story.profile_id != profile["id"]:
    return 'Forbidden', 403

  assoc = Association(**data)
  db.session.add(assoc)
  db.session.commit()

  story = Story.query.filter_by(id=story_id).first()
  return jsonify(story.serialize()), 201

@stories.errorhandler(Exception)          
def basic_error(err):
  return jsonify(err=str(err)), 500