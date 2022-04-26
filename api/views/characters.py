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