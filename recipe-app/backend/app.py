
from pathlib import Path

from flask import Flask
from flask_cors import CORS
from models import db
from routes.recipes import recipes_bp
from routes.groceries import groceries_bp

app = Flask(__name__, instance_relative_config=True)

Path(app.instance_path).mkdir(
    parents=True,
    exist_ok=True,
)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"sqlite:///{Path(app.instance_path) / 'recipes.db'}"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
CORS(app, resources={
    r"/api/*": {"origins": "http://localhost:5173"}
})

app.register_blueprint(
    recipes_bp,
    url_prefix="/api/recipes",
)
app.register_blueprint(
    groceries_bp,
    url_prefix="/api/groceries",
)

with app.app_context():
    db.create_all()


@app.get("/api/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(debug=True, port=4321)
