from database import db

class Usuario(db.Model):
    __tablename__ ='usuarios'
    id=db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(70),nullable=False,unique=True)
    clave = db.Column(db.String(100), nullable=False)


    def __init__(self, usuario, clave):
        self.usuario = usuario
        self.clave= clave


class Pelicula(db.Model):
    __tablename__ = 'peliculas'
    id=db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150),nullable=False,unique=True)
    
    director = db.Column(db.String(100)) 
     
    genero = db.Column(db.String(125))
       

    def __init__(self, nombre,  director,  genero):
        self.nombre = nombre
        
        self.director =director
        
        self.genero = genero
        
        