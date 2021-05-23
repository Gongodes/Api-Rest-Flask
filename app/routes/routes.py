from flask import Blueprint, request, jsonify, render_template, url_for,redirect

from database import db
from models.models import Usuario, Pelicula
from schema.schemas import peliculas_schema, pelicula_schema
import bcrypt
import requests
import json
import unicodedata


blue_print = Blueprint('app',__name__)

# Ruta de inicio


@blue_print.route('/inicio', methods=['GET'])
def inicio():
  info = requests.get('http://localhost:5000/api/peliculas')
  info = unicodedata.normalize('NFKD', info.text).encode('ascii','ignore')
  info = json.loads(info)
  return  render_template('index.html',info= info)

# Ruta de registro de usuario


@blue_print.route('/auth/registrar', methods=['POST','GET'])
def registrar_usuario():
  if request.method=="POST":
    
        # obtener usuario
        usuario = request.form.get('usuario')

        # obtener clave
        clave = request.form.get('clave')

       

        # consultar la db
        existe_usuario = Usuario.query.filter_by(usuario=usuario).first()

        

        # encripatmos clave usuario con bcrypt

        clave_encriptada = bcrypt.hashpw(clave.encode('utf-8'), bcrypt.gensalt())

        # Creamos el modelo a guardar en la bd

        nuevo_usuario = Usuario(usuario, clave_encriptada)

        db.session.add(nuevo_usuario)
        db.session.commit()

        return redirect(url_for('app.iniciar_sesion'))

    
  return render_template('registro.html')

# ruta para iniciar sesion

@blue_print.route('/', methods=['POST','GET'])
def iniciar_sesion():
  if request.method=="POST":
    

        # obtener usuario
        usuario = request.form.get('usuario')

        # obtener clave
        clave = request.form.get('clave')


        # consultar la db
        existe_usuario = Usuario.query.filter_by(usuario=usuario).first()

        if not existe_usuario:
            return render_template('login.html')

        es_clave_valida = bcrypt.checkpw(clave.encode(
            'utf-8'), existe_usuario.clave.encode('utf-8'))

       # validamos que sean iguales las claves

        if es_clave_valida:
           
           return redirect(url_for('app.inicio'))
        return redirect(url_for('app.iniciar_sesion'))

    
  return  render_template('login.html')



# ruta crear pelicula


@blue_print.route('/api/peliculas', methods=['POST'])

def crear_pelicula():
    
        nombre = request.form.get('nombre')
        
        director =request.form.get('director')
        
        genero = request.form.get('genero')
        

        nueva_pelicula = Pelicula(
            nombre,  director, genero)

        db.session.add(nueva_pelicula)
        db.session.commit()

        return  redirect(url_for('app.inicio'))


# ruta obtener peliculas
@blue_print.route('/api/peliculas', methods=['GET'])

def obtener_peliculas():
    
        peliculas = Pelicula.query.all()
        respuesta = peliculas_schema.dump(peliculas)

        return peliculas_schema.jsonify(respuesta)
   






 # ruta eliminar peliculas por id
@blue_print.route('/api/peliculas/<int:id>', methods=['POST'])

def eliminar_pelicula_por_id(id):
    
        pelicula = Pelicula.query.get(id)
        
        

        db.session.delete(pelicula)
        db.session.commit()
        return  redirect(url_for('app.inicio'))
    
                 
