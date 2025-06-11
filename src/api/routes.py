from flask import request, jsonify, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from api.models import db, User
from api.utils import APIException

api = Blueprint('api', __name__)

# Endpoints de autenticación (mantienen sus rutas originales)
@api.route('/signup', methods=['POST'])
def handle_signup():
    data = request.get_json()
    
    if not data.get('email') or not data.get('password'):
        return jsonify({"message": "Email y contraseña requeridos"}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"message": "Usuario ya existe"}), 400
    
    hashed_password = generate_password_hash(data['password'])
    new_user = User(
        email=data['email'],
        password=hashed_password,
        is_active=True
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"message": "Usuario creado exitosamente"}), 201

@api.route('/login', methods=['POST'])
def handle_login():
    data = request.get_json()
    
    user = User.query.filter_by(email=data.get('email')).first()
    if not user or not check_password_hash(user.password, data.get('password')):
        return jsonify({"message": "Email o contraseña inválidos"}), 401
    
    access_token = create_access_token(identity=str(user.id))
    return jsonify({ 
        "message": "Login exitoso",
        "token": access_token,
        "user_id": user.id
    }), 200

@api.route('/private', methods=['GET'])
@jwt_required()
def handle_private():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({"message": "Usuario no encontrado"}), 404
    
    return jsonify({
        "message": "Acceso privado concedido",
        "user_email": user.email
    }), 200