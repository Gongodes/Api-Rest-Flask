from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity,  jwt_required
from database import db
from models.models import Usuario, Pelicula
from schema.schemas import peliculas_schema, pelicula_schema
import bcrypt


blue_print = Blueprint('app',__name__)

# Ruta de inicio


@blue_print.route('/', methods=['GET'])
def inicio():
    return jsonify(respuesta='Rest API con Python, Flask y Mysql')

# Ruta de registro de usuario


@blue_print.route('/auth/registrar', methods=['POST'])
def registrar_usuario():
    try:
        # obtener usuario
        usuario = request.json.get('usuario')

        # obtener clave
        clave = request.json.get('clave')

        if not usuario or not clave:
            return jsonify(respuesta='campos invalidos'), 400

        # consultar la db
        existe_usuario = Usuario.query.filter_by(usuario=usuario).first()

        if existe_usuario:
            return jsonify(respuesta='usuario ya existe'), 400

        # encripatmos clave usuario con bcrypt

        clave_encriptada = bcrypt.hashpw(clave.encode('utf-8'), bcrypt.gensalt())

        # Creamos el modelo a guardar en la bd

        nuevo_usuario = Usuario(usuario, clave_encriptada)

        db.session.add(nuevo_usuario)
        db.session.commit()

        return jsonify(respuesta='usuario creado exitosamente'), 201

    except Exception:
        return jsonify(respuesta='Error en Peticion'), 500


# ruta para iniciar sesion

@blue_print.route('/auth/login', methods=['POST'])
def iniciar_sesion():
    try:

        # obtener usuario
        usuario = request.json.get('usuario')

        # obtener clave
        clave = request.json.get('clave')

        if not usuario or not clave:
            return jsonify(respuesta='campos invalidos'), 400

        # consultar la db
        existe_usuario = Usuario.query.filter_by(usuario=usuario).first()

        if not existe_usuario:
            return jsonify(respuesta='Usuario no encontrado'), 404

        es_clave_valida = bcrypt.checkpw(clave.encode(
            'utf-8'), existe_usuario.clave.encode('utf-8'))

       # validamos que sean iguales las claves

        if es_clave_valida:
           access_token = create_access_token(identity=usuario)
           return jsonify(access_token=access_token), 200
        return jsonify(respuesta='Clave o usuario Incorrecto'), 404

    except Exception:
        return jsonify(respuesta='Error en Peticion'), 500


""" RUTAS PROTEGIDAS POR JWT  """

# ruta crear pelicula


@blue_print.route('/api/peliculas', methods=['POST'])
@jwt_required()
def crear_pelicula():
    try:
        nombre = request.json.get('nombre')
        estreno = request.json.get('estreno')
        director = request.json.get('director')
        reparto = request.json.get('reparto')
        genero = request.json.get('genero')
        sinopsis = request.json.get('sinopsis')

        nueva_pelicula = Pelicula(
            nombre, estreno, director, reparto, genero, sinopsis)

        db.session.add(nueva_pelicula)
        db.session.commit()

        return jsonify(respuesta='pelicula Almacenada Exitosamente'), 201
    except Exception:
        return jsonify(respuesta='Error en Peticion'),500   


# ruta obtener peliculas
@blue_print.route('/api/peliculas', methods=['GET'])
@jwt_required()
def obtener_peliculas():
    try:
        peliculas = Pelicula.query.all()
        respuesta = peliculas_schema.dump(peliculas)

        return peliculas_schema.jsonify(respuesta), 200
    except Exception:
        return jsonify(respuesta='Error en Peticion'),500    



    # ruta obtener peliculas por id
@blue_print.route('/api/peliculas/<int:id>', methods=['GET'])
@jwt_required()
def obtener_pelicula_por_id(id):
    try:
        pelicula = Pelicula.query.get(id)
        

        return pelicula_schema.jsonify(pelicula), 200
    except Exception:
        return jsonify(respuesta='Error en Peticion'),500           



# ruta actualizar pelicula
@blue_print.route('/api/peliculas/<int:id>', methods=['PUT'])
@jwt_required()
def actualizar_pelicula(id):
    try:

        pelicula = Pelicula.query.get(id)

        if not pelicula:
            return jsonify(respuesta='pelicula no encontrada'), 404

        pelicula.nombre = request.json['nombre']
        pelicula.estreno = request.json['estreno']
        pelicula.director = request.json['director']
        pelicula.reparto = request.json['reparto']
        pelicula.genero = request.json['genero']
        pelicula.sinopsis = request.json['sinopsis']
        

        
        db.session.commit()

        return jsonify(respuesta='pelicula Actualizada Exitosamente'), 200
    except Exception:
        return jsonify(respuesta='Error en Peticion'),500 




 # ruta eliminar peliculas por id
@blue_print.route('/api/peliculas/<int:id>', methods=['DELETE'])
@jwt_required()
def eliminar_pelicula_por_id(id):
    try:
        pelicula = Pelicula.query.get(id)
        
        if not pelicula:
            return jsonify(respuesta='pelicula no encontrada'),404

        db.session.delete(pelicula)
        db.session.commit()
        return jsonify(respuesta='pelicula eliminada exitosamente'),200
    except Exception:
        return jsonify(respuesta='Error en Peticion'),500           
