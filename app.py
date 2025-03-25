from flask import Flask
from extensions import db, login_manager
from routes.signup import signup_bp
from routes.login import login_bp
from routes.products import products_bp
from routes.order import order_bp

# Import models
from models.customer import Customer
from models.product import Product, ProductImage
from models.order import OrderHistory, OrderHistoryItem

# Initialize Flask app
app = Flask(__name__)

# Configure MySQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://kavangajera:kg123@localhost/ecom-project'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this to a secure secret key

# Initialize extensions
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login.login'

@login_manager.user_loader
def load_user(user_id):
    return Customer.query.get(int(user_id))

# Register blueprints
app.register_blueprint(signup_bp)
app.register_blueprint(login_bp)
app.register_blueprint(products_bp)
app.register_blueprint(order_bp)

if __name__ == '__main__':
    app.run(debug=True)
