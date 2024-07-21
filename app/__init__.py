from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask import render_template

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from app.routes import product, supplier, employee, purchase, sale, inventory, analysis
    app.register_blueprint(product.bp)
    app.register_blueprint(supplier.bp)
    app.register_blueprint(employee.bp)
    app.register_blueprint(purchase.bp)
    app.register_blueprint(sale.bp)
    app.register_blueprint(inventory.bp)
    app.register_blueprint(analysis.bp)

    @app.route('/')
    def index():
        return render_template('index.html')

    return app