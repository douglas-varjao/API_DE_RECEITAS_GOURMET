#app
from flask import Flask, jsonify, request

app = Flask(__name__)

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