@app.route('/rentas', methods = ['POST'])
def create_renta():
    # recibiendo informacion 
    id_socio = request.json['id_socio']
    id_peli_serie = request.json['id_peli_serie']
    fecha_inicio_renta = request.json['fecha_inicio_renta']
    fecha_fin_renta = request.json['fecha_fin_renta']
        
    id = mongo.db.Rentas.insert( 
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
    rentas = mongo.db.Rentas.find()
    response = dumps(rentas)
    return Response(response, mimetype="aplication/json")

@app.route('/rentas/<id>', methods=['GET'])
def get_renta(id):
    renta = mongo.db.Rentas.find_one({'Id_socio': id})
    response = dumps(renta)
    return Response(response, mimetype="aplication/json")

@app.route('/rentas/<id>', methods=['DELETE'])
def delete_renta(id):
    mongo.db.Rentas.delete_one({'Id_socio': id})
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
        
        mongo.db.Rentas.update_one({'Id_socio': id}, {'$set':{
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
