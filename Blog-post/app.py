from flask import Flask
from db import create_tables
from routes import register_blueprints

app = Flask(__name__)
app.secret_key = "hello"

register_blueprints(app)

if __name__ == "__main__":
    create_tables()
    app.run(debug=True)
