from .auth import auth_blueprint
from .blog import blog_blueprint
from .admin import admin_blueprint
from .home import home_blueprint  # Import the home blueprint

def register_blueprints(app):
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(blog_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(home_blueprint)  # Register the home blueprint
