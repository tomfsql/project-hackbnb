from flask import Blueprint, request, send_from_directory

uploads_api = Blueprint('uploads', __name__)

@uploads_api.route('/')
def get_upload():
   name = request.args.get("name")
   if not name:
      return {'error': 'Missing name'}, 400
   # send_from_directory refuse tout chemin qui sort du dossier (404)
   return send_from_directory('uploads', name)