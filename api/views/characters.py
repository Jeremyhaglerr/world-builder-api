from flask import Blueprint, jsonify, request
from api.middleware import login_required, read_token

from api.models.db import db
from api.models.character import Character

characters = Blueprint('characters', 'characters')

@characters.route('/', methods=["POST"]) 
@login_required
def create():
  data = request.get_json()
  profile = read_token(request)
  data["profile_id"] = profile["id"]

  character = Character(**data)
  db.session.add(character)
  db.session.commit()
  return jsonify(character.serialize()), 201

@characters.route('/', methods=["GET"])
def index():
  characters = Character.query.all()
  return jsonify([character.serialize() for character in characters]), 201

@characters.route('/<id>', methods=["GET"])
def show(id):
  character = Character.query.filter_by(id=id).first()
  return jsonify(character.serialize()), 200
