#app
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flasgger import Swagger

#importo config:

from config import Config

#cria instancia da aplicação flask e configura com o config
app = Flask(__name__)
app.config.from_object(Config)

#inicia as extensões
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
swagger = Swagger(app)

#----- BANCO DE DADOS ----

class User(db.Model):
    """ 
    Modelo de dados para a tabela de usuario.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)
    #Relação das receitas: um usuario pode ter muitas receitas
    recipes = db.relationship('Recipe', beckref='author', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

class Recipe(db.Model):
    """
    Modelo de dados para a tabela de receitas
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False) 
    description = db.Column(db.Text, nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    #relação do usuario com a receita por ID
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)

    def __repr__(self):
        return f'<Recipe {self.title}>'
    
#-----------Rotas----------------------------


@app.route('/')
def home():
    return "API de Receitas Gourmet está online!"
#--------------------------------------------------------------------------------------------

#--ROTAS USUARIOS--

#rota para registrar um novo usuario
@app.route('/users/registers', methods=['POST'])
def register():
    #logica
    return jsonify({"message": "Rota de registro de usuario em (desenvolvimento)"})

#rota para fazer login de um usuario 
@app.route('/users/login', methods=['POST'])
def login():
    #logica
    return jsonify({"message":"Rota de login de usuario em (desenvolvimento)"})
#------------------------------------------------------------------------------------------------

#--ROTAS DE RECEITAS--

#rota para obter todas as receitas:
@app.route('/recipes', methods=['GET'])
def get_recipes():
    #logica
    return({"message":"rota em desenvolvimento"})

#rota para adicionar nova receita:
@app.route('/recipes', methods=['POST'])
def post_recipes():
    #logica
    return ({"message":"rota em desenvolvimento"})

#rota para receber a receita por ID:
@app.route('/recipes/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    #logica
    return({"message": f"{recipe_id} em desenvolvimento"})

#rota para atualizar um receita existente:
@app.route('/recipes/<int:recipe_id>', methods=['PUT'])
def update_recipe(recipe_id):
    #logica
    return({"message":f"a receita {recipe_id} foi atualizada com sucesso (em desenvolvimento)"})

@app.route('/recipes/<int:recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    #logica
    return ({"message": f"a receita {recipe_id} foi deletada (em desenvolvimento)"})
#-------------------------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)