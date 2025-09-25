import os

class Config:
    """
    Classe de configuração base.
    Contem as configurações comuns para todas as instancias."""

    #a chave secreta é usada para assinar o token JWT
    #é importante usar uma chave complexa e manter segura
    SECRET_KEY = os.environ.get("SECRET_KEY") or 'voce-nunca-vai-adivinhar-esta-chave'


    SWAGGER = {
        'title': 'API de Receitas Gourmet',
        'uiversion': 3,
        "swagger_ui_bundle_js": "//unpkg.com/swagger-ui-dist@3/swagger-ui-bundle.js",
        "swagger_ui_standalone_preset_js": "//unpkg.com/swagger-ui-dist@3/swagger-ui-standalone-preset.js",
        "swagger_ui_css": "//unpkg.com/swagger-ui-dist@3/swagger-ui.css",
        "swagger_ui_fav_icon_css": "//unpkg.com/swagger-ui-dist@3/favicon-32x32.png"
    }

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'recipes.db')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    JWT_SECRET_KEY = 'minha_chave_jwt_secreta'