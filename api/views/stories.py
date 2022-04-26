from flask import Blueprint, jsonify, request
from api.middleware import login_required, read_token

from api.models.db import db
from api.models.story import Story

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
  return jsonify(story=story_data), 200