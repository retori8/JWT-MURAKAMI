"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Books
from api.utils import generate_sitemap, APIException

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from werkzeug.security import generate_password_hash, check_password_hash

api = Blueprint('api', __name__)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

@api.route('/api/registro', methods=['POST'])
def register():

    user = User()
    user.email = request.json.get("email")
    user.password = generate_password_hash(request.json.get("password"))
    
    
    if not user.email:
        return jsonify({ "msg": "Necesitamos tu email"}), 422

    if not user.password:
        return jsonify({ "msg": "Necesitamos que ingreses una contraseña"}), 422

    user_filter = User.query.filter_by(email=user.email).first()

    if user_filter:
        return jsonify({ "msg": "El usuario ya existe"}), 400

    user.new_user()
    
    return jsonify({"msg":"register created", "user": user.serialize()}), 201    
    
#LOGIN CON TOKEN--------------------------------------------------------------------

@api.route("/api/login", methods=["POST"])
def login_token():
    email = request.json.get("email")
    password = request.json.get("password")
    # Consulta la base de datos por el nombre de usuario y la contraseña
    user = User.query.filter_by(email=email).first()
    if user is None:
          # el usuario no se encontró en la base de datos
        return jsonify({"msg": "Email/Contraseña son incorrectos"}), 401
    
    # crea un nuevo token con el id de usuario dentro
    access_token = create_access_token(identity=user.id)
    return jsonify({ "token": access_token, "user_id": user.id })  
 

@api.route('/api/users', methods=['GET'])
def get_all_users():#trae todos los registros que tengo en mi base de datos
    users = User.query.all()
    users = list(map(lambda user: user.serialize(), users))#por cada usuario que encuentre llame a serialize que me permite convertirlo en un objeto serializado para ser reconocido por python

    return jsonify(users), 200  

#BOOKS-------------------------------------------------------------------------------           

@api.route('/api/libros', methods=['POST'])
def add_book():
    data = request.get_json()

    book = Books()
    book.title = data["title"]
    book.year = data["year"]
    book.image_url = data["image_url"]
    book.new_book()  

    return jsonify({"msg":"book created"}), 201

@api.route('/api/libros', methods=['GET'])
@jwt_required()
def get_all_books():

    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user:
        return jsonify({ "msg": "Necesitamos tu registro/acceso"}), 422

    else:    
    
        books = Books.query.all()
        books = list(map(lambda book: book.serialize(), books))

        return jsonify(books), 200      
