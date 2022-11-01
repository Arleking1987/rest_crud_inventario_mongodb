from asyncio.windows_events import NULL
from constants import DB_URI
from flask import Flask, make_response, request, jsonify
from flask_mongoengine import MongoEngine
from routes.auth import routes_auth
from dotenv import load_dotenv
from routes.users_github import users_github
from funcion_jwt import valida_token
from flask_cors import CORS, cross_origin




app = Flask(__name__)

CORS(app)

DB_URL = DB_URI
app.config["MONGODB_HOST"] = DB_URL

db = MongoEngine()
db.init_app(app)

class Product(db.Document):
    product_id = db.IntField()
    product_name = db.StringField()
    product_estado = db.StringField()
    product_tipeProduct = db.StringField()
    product_quantity = db.IntField()
    product_description = db.StringField()
    product_image = db.StringField()
    
    
 
 #Convertir el objeto a json   
def to_json(self):
     return   {
         "product_id": self.pruct_id,
         "product_name": self.product_name,
         "product_estado": self.product_estado,
         "product_tipeProduct": self.product_tipeProduct,
         "product_quantity": self.product_quantity,
         "product_description": self.product_description,
         "product_image": self.product_image
     }
     

# @app.before_request
# def verify_token_middleware():
#     token = request.headers['Authorization'].split(" ")[1]
#     valida_token(token, output=False)

#Obtener los productos con GET o ingresar un nuevo producto con POST
@cross_origin
@app.route('/api/productos', methods=['GET', 'POST'])
def obtenerProductos():
    # token = request.headers['Authorization'].split(" ")[1]
    # response=valida_token(token, output=True)
    # if response.status_code == 200:
        if request.method == "GET":
            productos = []
            for producto in Product.objects:
                productos.append(producto)
            return make_response(jsonify(productos), 200)
        elif request.method == "POST":
            content = request.json
            producto = Product(product_id = content['product_id'],
                                product_name = content['product_name'],
                                product_estado = content['product_estado'],
                                product_tipeProduct = content['product_tipeProduct'],
                                product_quantity = content['product_quantity'],
                                product_description = content['product_description'],
                                product_image = content['product_image'])
            producto.save()
            return make_response("", 201)       
    # else:
    #     return response
        
    
    
    
    
 #Obtener un registro segun el id con GET, actualizar un registro con PUT o borrar un registro con DELETE 
@cross_origin  
@app.route('/api/productos/<product_id>', methods=['GET', 'PUT', 'DELETE'])
def productoPorId(product_id):
    # token = request.headers['Authorization'].split(" ")[1]
    # response=valida_token(token, output=True)
    # if response.status_code == 200:
        if request.method == "GET":
            product_obj = Product.objects(product_id=product_id).first()
            if product_obj:
                return make_response(jsonify(product_obj), 200)
            else:
                return make_response("Producto no encontrado", 404)
        elif request.method == "PUT":
            content = request.json
            product_obj = Product.objects(product_id=product_id).first()
            product_obj.update(product_name = content['product_name'],
                                product_estado = content['product_estado'],
                                product_tipeProduct = content['product_tipeProduct'],
                                product_quantity = content['product_quantity'],
                                product_description = content['product_description'],
                                product_image = content['product_image'])
            return make_response("", 204)
        elif request.method == "DELETE":
            product_obj = Product.objects(product_id=product_id).first()
            product_obj.delete()
            return make_response()
    # else:
    #     return response 
         
        
app.register_blueprint(routes_auth, url_prefix="/token") 
app.register_blueprint(users_github, url_prefix="/token")
    
if __name__ == '__main__':
    load_dotenv()
    app.run()