#app
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
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
    recipes = db.relationship('Recipe', backref='author', lazy=True)

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
    """
    Endpoint para registro de novo usuário.
    ---
    tags:
      - Usuários
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: UserRegistration
          required:
            - username
            - password
          properties:
            username:
              type: string
              description: Nome de usuário único.
            password:
              type: string
              description: Senha para o usuário.
    responses:
      201:
        description: Usuário registrado com sucesso.
      400:
        description: Nome de usuário já existe ou dados ausentes.
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Nome de usuario e senha são obrigatórios"}), 400
    
    if User.query.filter_by(username=username).first():
            return jsonify({"message": "Nome de usuario ja existe"}), 400
    
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, password=hashed_password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Usuario registrado com sucesso" }), 201


#rota para fazer login de um usuario 
@app.route('/users/login', methods=['POST'])
def login():
    """
    Endpoint para login de usuario.
    ---
    tags:
      - Usuarios
    parametes:
      - name: body
        in: body
        required: true
        schema:
          id: UserLogin
          required:
            - username
            - password
          properties:
            username:
              type: string
              description: Nome de usuario.
            password:
              type: string
              description: Senha.
    responses:
      200:
        description: Login bem-sucedido, retorna um token de acesso.
        schema:
          properties:
            access_token:
              type: string
              description: Token JWT para autenticação.
      401:
        description: Nome de usuario ou senha incorretos   
    """

    data = request.get_json()
    usename = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(usename=usename).first()

    if user and bcrypt.check_password_hash(user.password, password):
        #a identidade do token sera o id de usuario
        access_token= create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"message":"Nome de usuario ou senha incorretos"}), 401
#------------------------------------------------------------------------------------------------

#--ROTAS DE RECEITAS--

#rota para obter todas as receitas:
@app.route('/recipes', methods=['GET'])
def get_recipes():
    """
    Obtém todas as receitas.
    ---
    tags:
      - Receitas
    responses:
      200:
        description: Retorna um lista de todas as receitas.
        schema:
          type: array
          items:
            properties:
              id:
                type: integer
              title:
                type: string
              description:
                type: string
              ingredients:
                type: string
              instructions:
                type: string
              user_id:
                type: integer
    """
    recipes = Recipe.query.all()
    output = []
    for recipe in recipes:
        recipe_data = {}
        recipe_data['id'] = recipe.id
        recipe_data['title'] = recipe.title
        recipe_data['description'] = recipe.description
        recipe_data['ingredients'] = recipe.ingredients
        recipe_data['instructions'] = recipe.instructions
        recipe_data['user_id'] = recipe.user_id
        output.append(recipe_data)

    return jsonify({"recipes": output})

#rota para adicionar nova receita:
@app.route('/recipes', methods=['POST'])
def post_recipes():
    """
    Adiciona uma nova receita
    ---
    tags:
      - Receiras
    security:
      - JWT: []
    parameters:
      - name: body
        in: body 
        required: true
        schema:
          id: NewRecipe
          required:
            - title
            - description
            - instruction
          properties:
            title:
              type: string
              description: Titulo da receita.
            description:
              type: string
              description: Descrição da receita.
            ingredients:
              type: string
            instructions:
              type: string
              description: Instruções de preparo.
    responses:
      201:
        description: Receira criada com sucesso.
      401:
        description: Token JWT ausente ou invalido.
      400:
        description: Dados ausentes no corpo da requisição.
    """
    data = request.get_json()
    #pega o ID do usuario apartir do token JWT
    current_user_id = get_jwt_identity()

    if not data or not data.get('title') or not data.get('description') or not data.get('ingredients') or not data.get('instructions'):
      return jsonify({"message":"Dadis incompletos para a receita"}), 400
    
    new_recipe = Recipe(
        title=data['title'],
        description=data['description'],
        ingredients=data['ingredients'],
        instructions=data['instructions'],
        user_id=current_user_id
    )
    db.session.add(new_recipe)
    db.session.commit()
    return jsonify({"message":"Receita adicionada com sucesso!", "recipe_id":new_recipe.id}), 201


#rota para receber a receita por ID:
@app.route('/recipes/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    """
    Obtem uma receita especifica pelo ID.
    ---
    tags:
      - name: recipe_id
        in: path
        type: integer
        required: true
        description: ID da receita.
    responses:
      200:
        description: Retorna os detalhes da receita.
      400:
        description: Receirta não encontrada.
    """
    recipe = Recipe.query.get_or_404(recipe_id)
    return jsonify ({
        "id": recipe_id,
        "tile": recipe.title,
        "description": recipe.description,
        "ingredients": recipe.ingredients,
        "instructions": recipe.instructions,
        "user_id": recipe.user_id
    })

#rota para atualizar um receita existente:
@app.route('/recipes/<int:recipe_id>', methods=['PUT'])
def update_recipe(recipe_id):
    """
    Atualiza uma receita existente.
    ---
    tags:
      - Receitas
    security:
      - JWT: []
    parameters:
      - name: recipe_id
        in: path
        type: integer
        required: true
        description: ID da receita a ser atualizada.
      - name: body
        in: body
        required: true
        schema:
          id: UpdateRecipe
          properties:
            title:
              type: string
            description:
              type: string
            ingredients:
              type: string
            instructions:
              type: string
    responses:
      200:
        description: Receita atualizada com sucesso.
      401:
        description: Token JWT ausente ou inválido.
      403:
        description: Você não tem permissão para atualizar esta receita.
      404:
        description: Receita não encontrada.
    """
    return({"message":f"a receita {recipe_id} foi atualizada com sucesso (em desenvolvimento)"})

@app.route('/recipes/<int:recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    #logica
    return ({"message": f"a receita {recipe_id} foi deletada (em desenvolvimento)"})
#-------------------------------------------------------------------------------------------

@app.cli.command("creat-db")
def create_db():
    """ Cria as tabelas do banco de dados a partir dos modelos."""
    with app.app_context():
        db.create_all()
        print("Banco de dados e tabelas criados com sucesso")

if __name__ == "__main__":
    app.run(debug=True)