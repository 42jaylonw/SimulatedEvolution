from flask import Flask

# Create application
def create_app():
    app = Flask(__name__)
    
    # register  route blueprints from views
    from .views import views
    app.register_blueprint(views, url_prefix="/")
    #NOTE: consider app.config to generate private session keys for users
    return app