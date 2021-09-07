from flask import Flask, jsonify, request, Response
from flask_pymongo import PyMongo
from bson.json_util import dumps
from pymongo import message
from flask_cors import CORS
#from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
import json
import random

from werkzeug.wrappers import response

app = Flask(__name__)
cors = CORS(app , resources = {r"/*":{"origins":"*"}}) 
app.config['MONGO_URI'] = 'mongodb://localhost:27017/Proyecto-Inv' # directorio de mi base de datos local
mongo = PyMongo(app)

    ## ENDPOINTS DE SOCIOS ##

@app.route('/socios', methods = ['POST'])
def create_socio():
    # recibiendo informacion 
    id_socio = random.randrange(5011)
    nombre = request.json['Nombre']
    apellidos = request.json['Apellidos']
    contrasenia = request.json['Contrasenia']
    correo =  request.json['Correo']
    telefono =  request.json['Telefono']
    hashed_password = generate_password_hash(contrasenia)
    id = mongo.db.Socios.insert( 
        {'Id_socio': id_socio,
         'Nombre': nombre,
         'Apellidos': apellidos,
         'Contrasenia': hashed_password,
         'Correo': correo,
         'Telefono': telefono
        }
    ) 
    response = jsonify({
        '_id':str(id), 
        'Id_socio': id_socio,
        'Nombre': nombre,
        'Apellidos': apellidos,
        'Contrasenia': contrasenia,
        'Correo': correo,
        'Telefono': telefono
    })
    response.status_code = 201 
    return response # respuesta en JSON al agregar socio nuevo

@app.route('/socios', methods=['GET'])
def get_socios():
    socios = mongo.db.Socios.find()
    response = dumps(socios)
    return Response(response, mimetype="aplication/json")

@app.route('/socios/<id>', methods=['GET'])
def get_socio(id):
    socio = mongo.db.Socios.find_one({'Id_socio': id})
    response = dumps(socio)
    return Response(response, mimetype="aplication/json")

@app.route('/socios/<id>', methods=['DELETE'])
def delete_socio(id):
    mongo.db.Socios.delete_one({'Id_socio': id})
    response = jsonify({'Message': 'Socio ' + id + ' borrado exitosamente'})
    response.status_code = 200 
    return response

@app.route('/socios/<id>', methods=['PUT'])
def update_socio(id):
    nombre = request.json['nombre']
    apellidos = request.json['apellidos']
    contrasenia = request.json['contrasenia']
    correo =  request.json['correo']
    telefono =  request.json['telefono']
    if nombre and apellidos and contrasenia and correo and telefono and id:
        hashed_password = generate_password_hash(contrasenia)
        mongo.db.Socios.update_one({'Id_socio': id}, {'$set':{
        'Nombre': nombre,
        'Apellidos': apellidos,
        'Contrasenia': hashed_password,
        'Correo': correo,
        'Telefono': telefono
        }})
        response = jsonify({'Message': 'Socio ' + id + ' actualizado exitosamente'})
        response.status_code = 200 
        return response
    else:
        return not_found()

        ## ENDPOINTS FORMA DE PAGO ##

@app.route('/pagos', methods = ['POST'])
def create_pago():
    # recibiendo informacion 
    id_socio = request.json['id_socio']
    id_tarjeta = request.json['id_tarjeta']
    codigo = request.json['codigo']
    fecha_vencimiento = request.json['fecha_vencimiento']
    hashed_codigo = generate_password_hash(codigo)
    id = mongo.db.Forma_Pago.insert( 
        {'Id_socio': id_socio,
         'Id_tarjeta': id_tarjeta,
         'Codigo': hashed_codigo ,
         'Fecha_vencimiento': fecha_vencimiento
        }
    ) 
    response = jsonify({
        '_id':str(id), 
        'Id_socio': id_socio,
        'Id_tarjeta': id_tarjeta,
        'Codigo': codigo,
        'Fecha_vencimiento': fecha_vencimiento
    })
    response.status_code = 201 
    return response # respuesta en JSON al agregar pago nuevo

@app.route('/pagos', methods=['GET'])
def get_pagos():
    pagos = mongo.db.Forma_Pago.find()
    response = dumps(pagos)
    return Response(response, mimetype="aplication/json")

@app.route('/pagos/<id>', methods=['GET'])
def get_pago(id):
    pago = mongo.db.Forma_Pago.find_one({'Id_socio': id})
    response = dumps(pago)
    return Response(response, mimetype="aplication/json")

@app.route('/pagos/<id>', methods=['DELETE'])
def delete_pago(id):
    mongo.db.Forma_Pago.delete_one({'Id_socio': id})
    response = jsonify({'Message': 'Pago ' + id + ' borrado exitosamente'})
    response.status_code = 200 
    return response

@app.route('/pagos/<id>', methods=['PUT'])
def update_pago(id):
    id_tarjeta = request.json['id_tarjeta']
    codigo = request.json['codigo']
    fecha_vencimiento = request.json['fecha_vencimiento']
    if id_tarjeta and codigo and fecha_vencimiento and id:
        hashed_codigo = generate_password_hash(codigo)
        mongo.db.Forma_Pago.update_one({'Id_socio': id}, {'$set':{
        'Id_tarjeta': id_tarjeta,
        'Codigo': hashed_codigo,
        'Fecha_vencimiento': fecha_vencimiento
        }})
        response = jsonify({'Message': 'Pago ' + id + ' actualizado exitosamente'})
        response.status_code = 200 
        return response
    else:
        return not_found()

        ## ENDPOINTS PELICULAS ##

@app.route('/peliculas', methods = ['POST'])
def create_pelicula():
    # recibiendo informacion 
    id_pelicula = request.json['id_pelicula']
    titulo = request.json['titulo']
    descripcion = request.json['descripcion']
    duracion = request.json['duracion']
    categoria = request.json['categoria']
    fecha_estreno = request.json['fecha_estreno']
    url_imagen = request.json['url_imagen']
    
    id = mongo.db.Peliculas.insert( 
        {
         'Id_pelicula': id_pelicula,
         'Titulo': titulo,
         'Descripcion': descripcion,
         'Duracion': duracion,
         'Categoria': categoria,
         'Fecha_estreno': fecha_estreno,
         'Url_imagen': url_imagen
        }
    ) 
    response = jsonify({
        'Id_pelicula': id_pelicula,
         'Titulo': titulo,
         'Descripcion': descripcion,
         'Duracion': duracion,
         'Categoria': categoria,
         'Fecha_estreno': fecha_estreno,
        'Url_imagen': url_imagen
    })
    response.status_code = 201 
    return response # respuesta en JSON al agregar pelicula nuevo

@app.route('/peliculas', methods=['GET'])
def get_peliculas():
    peliculas = mongo.db.Peliculas.find()
    response = dumps(peliculas)
    return Response(response, mimetype="aplication/json")

@app.route('/peliculas/<id>', methods=['GET'])
def get_pelicula(id):
    pelicula = mongo.db.Peliculas.find_one({'Id_pelicula': id})
    response = dumps(pelicula)
    return Response(response, mimetype="aplication/json")

@app.route('/peliculas/<id>', methods=['DELETE'])
def delete_pelicula(id):
    mongo.db.Peliculas.delete_one({'Id_pelicula': id})
    response = jsonify({'Message': 'Pago ' + id + ' borrado exitosamente'})
    response.status_code = 200 
    return response

@app.route('/peliculas/<id>', methods=['PUT'])
def update_pelicula(id):
    id_pelicula = request.json['id_pelicula']
    titulo = request.json['titulo']
    descripcion = request.json['descripcion']
    duracion = request.json['duracion']
    categoria = request.json['categoria']
    fecha_estreno = request.json['fecha_estreno']
    url_imagen = request.json['url_imagen']
    if titulo and descripcion and categoria and duracion and fecha_estreno and id:
        
        mongo.db.Peliculas.update_one({'Id_pelicula': id}, {'$set':{
        'Id_pelicula': id_pelicula,
         'Titulo': titulo,
         'Descripcion': descripcion,
         'Duracion': duracion,
         'Categoria': categoria,
         'Fecha_estreno': fecha_estreno,
         'Url_imagen': url_imagen
        }})
        response = jsonify({'Message': 'Pago ' + id + ' actualizado exitosamente'})
        response.status_code = 200 
        return response
    else:
        return not_found()

        ## ENDPOINTS SERIES ##

@app.route('/series', methods = ['POST'])
def create_serie():
    # recibiendo informacion 
    id_serie = request.json['id_serie']
    titulo = request.json['titulo']
    descripcion = request.json['descripcion']
    capitulos = request.json['capitulos']
    temporadas = request.json['temporadas']
    categoria = request.json['categoria']
    fecha_estreno = request.json['fecha_estreno']
    url_imagen = request.json['url_imagen']
    
    id = mongo.db.Series.insert( 
        {
         'Id_serie': id_serie,
         'Titulo': titulo,
         'Descripcion': descripcion,
         'Capitulos': capitulos,
         'Temporadas': temporadas,
         'Categoria': categoria,
         'Fecha_estreno': fecha_estreno,
         'Url_imagen': url_imagen
        }
    ) 
    response = jsonify({
        'Id_serie': id_serie,
         'Titulo': titulo,
         'Descripcion': descripcion,
         'Capitulos': capitulos,
         'Temporadas': temporadas,
         'Categoria': categoria,
         'Fecha_estreno': fecha_estreno,
         'Url_imagen': url_imagen
    })
    response.status_code = 201 
    return response # respuesta en JSON al agregar serie nuevo

@app.route('/series', methods=['GET'])
def get_series():
    series = mongo.db.Series.find()
    response = dumps(series)
    return Response(response, mimetype="aplication/json")

@app.route('/series/<id>', methods=['GET'])
def get_serie(id):
    serie = mongo.db.Series.find_one({'Id_serie': id})
    response = dumps(serie)
    return Response(response, mimetype="aplication/json")

@app.route('/series/<id>', methods=['DELETE'])
def delete_serie(id):
    mongo.db.Series.delete_one({'Id_serie': id})
    response = jsonify({'Message': 'Pago ' + id + ' borrado exitosamente'})
    response.status_code = 200 
    return response

@app.route('/series/<id>', methods=['PUT'])
def update_serie(id):
    id_serie = request.json['id_serie']
    titulo = request.json['titulo']
    descripcion = request.json['descripcion']
    capitulos = request.json['capitulos']
    temporadas = request.json['temporadas']
    categoria = request.json['categoria']
    fecha_estreno = request.json['fecha_estreno']
    url_imagen = request.json['url_imagen']
    if titulo and descripcion and categoria and capitulos and fecha_estreno and id:
        
        mongo.db.Series.update_one({'Id_serie': id}, {'$set':{
        'Id_serie': id_serie,
         'Titulo': titulo,
         'Descripcion': descripcion,
         'Capitulos': capitulos,
         'Temporadas': temporadas,
         'Categoria': categoria,
         'Fecha_estreno': fecha_estreno,
         'Url_imagen': url_imagen
        }})
        response = jsonify({'Message': 'Pago ' + id + ' actualizado exitosamente'})
        response.status_code = 200 
        return response
    else:
        return not_found()

    ## ENDPOINT CAPITULOS ##

@app.route('/capitulos', methods = ['POST'])
def create_capitulo():
    # recibiendo informacion 
    id_capitulo = request.json['id_capitulo']
    id_serie = request.json['id_serie']
    temporadas = request.json['temporadas']
    titulo = request.json['titulo']
    descripcion =  request.json['descripcion']
    duracion =  request.json['duracion']
    
    id = mongo.db.Capitulos.insert( 
        {'Id_capitulo': id_capitulo,
         'Id_serie': id_serie,
         'Temporadas': temporadas,
         'Titulo': titulo,
         'Descripcion': descripcion,
         'Duracion': duracion
        }
    ) 
    response = jsonify({
        '_id':str(id), 
        'Id_capitulo': id_capitulo,
        'Id_serie': id_serie,
        'Temporadas': temporadas,
        'Titulo': titulo,
        'Descripcion': descripcion,
        'Duracion': duracion
    })
    response.status_code = 201 
    return response # respuesta en JSON al agregar capitulo nuevo

@app.route('/capitulos', methods=['GET'])
def get_capitulos():
    capitulos = mongo.db.Capitulos.find()
    response = dumps(capitulos)
    return Response(response, mimetype="aplication/json")

@app.route('/capitulos/<id>', methods=['GET'])
def get_capitulo(id):
    capitulo = mongo.db.Capitulos.find_one({'Id_capitulo': id})
    response = dumps(capitulo)
    return Response(response, mimetype="aplication/json")

@app.route('/capitulos/<id>', methods=['DELETE'])
def delete_capitulo(id):
    mongo.db.Capitulos.delete_one({'Id_capitulo': id})
    response = jsonify({'Message': 'Capitulo ' + id + ' borrado exitosamente'})
    response.status_code = 200 
    return response

@app.route('/capitulos/<id>', methods=['PUT'])
def update_capitulo(id):
    id_capitulo = request.json['id_capitulo']
    id_serie = request.json['id_serie']
    temporadas = request.json['temporadas']
    titulo = request.json['titulo']
    descripcion =  request.json['descripcion']
    duracion =  request.json['duracion']
    if id_capitulo and id_serie and temporadas and titulo and descripcion and duracion and id:
        
        mongo.db.Capitulos.update_one({'Id_capitulo': id}, {'$set':{
        'Id_capitulo': id_capitulo,
        'Id_serie': id_serie,
        'Temporadas': temporadas,
        'Titulo': titulo,
        'Descripcion': descripcion,
        'Duracion': duracion
        }})
        response = jsonify({'Message': 'Capitulo ' + id + ' actualizado exitosamente'})
        response.status_code = 200 
        return response
    else:
        return not_found()

    ## ENDPOINTS RENTA ##

@app.route('/rentas', methods = ['POST'])
def create_renta():
    # recibiendo informacion 
    id_socio = request.json['id_socio']
    id_peli_serie = request.json['id_peli_serie']
    fecha_inicio_renta = request.json['fecha_inicio_renta']
    fecha_fin_renta = request.json['fecha_fin_renta']
        
    id = mongo.db.Renta.insert( 
        {
         'Id_socio': id_socio,
         'Id_peli_serie': id_peli_serie,
         'Fecha_inicio_renta': fecha_inicio_renta,
         'Fecha_fin_renta': fecha_fin_renta,
        }
    ) 
    response = jsonify({
        '_id':str(id), 
        'Id_socio': id_socio,
        'Id_peli_serie': id_peli_serie,
        'Fecha_inicio_renta': fecha_inicio_renta,
        'Fecha_fin_renta': fecha_fin_renta,
    })
    response.status_code = 201 
    return response # respuesta en JSON al agregar renta nuevo

@app.route('/rentas', methods=['GET'])
def get_rentas():
    rentas = mongo.db.Renta.find()
    response = dumps(rentas)
    return Response(response, mimetype="aplication/json")

@app.route('/rentas/<id>', methods=['GET'])
def get_renta(id):
    renta = mongo.db.Renta.find_one({'Id_socio': id})
    response = dumps(renta)
    return Response(response, mimetype="aplication/json")

@app.route('/rentas/<id>', methods=['DELETE'])
def delete_renta(id):
    mongo.db.Renta.delete_one({'Id_socio': id})
    response = jsonify({'Message': 'Capitulo ' + id + ' borrado exitosamente'})
    response.status_code = 200 
    return response

@app.route('/rentas/<id>', methods=['PUT'])
def update_renta(id):
    id_socio = request.json['id_socio']
    id_peli_serie = request.json['id_peli_serie']
    fecha_inicio_renta = request.json['fecha_inicio_renta']
    fecha_fin_renta = request.json['fecha_fin_renta']
    
    if id_socio and id_peli_serie and fecha_inicio_renta and fecha_fin_renta and id:
        
        mongo.db.Renta.update_one({'Id_socio': id}, {'$set':{
            'Id_socio': id_socio,
            'Id_peli_serie': id_peli_serie,
            'Fecha_inicio_renta': fecha_inicio_renta,
            'Fecha_fin_renta': fecha_fin_renta,
        }})
        response = jsonify({'Message': 'Capitulo ' + id + ' actualizado exitosamente'})
        response.status_code = 200 
        return response
    else:
        return not_found()

@app.errorhandler(404)
def not_found(error = None):
    message = {'Message': 'Recurso no encontrado' + request.url, 'Status':404}
    response = jsonify(message)
    response.status_code = 404
    return response

if __name__ == "__main__":
    app.run(debug = True) # aqui se especifica que se van a 
                          # correr los servicios como 
                          # debug (cambiar a false cuando se pase a produccion)