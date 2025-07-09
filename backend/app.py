from flask import Flask, jsonify, request, send_from_directory
from models import db, Coffee, Product, CartItem, Review
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'frontend_uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/static/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/')
def index():
    return jsonify({"message": "Gila Kopi Backend API is running."})

# ---------------- Menu Endpoints ----------------
@app.route('/api/menu', methods=['GET', 'POST'])
def menu():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        description = request.form.get('description', '')

        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400

        file = request.files['image']
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        image_url = f"/static/uploads/{filename}"

        coffee = Coffee(name=name, price=price, description=description, image_url=image_url)
        db.session.add(coffee)
        db.session.commit()
        return jsonify({'message': 'Coffee added successfully.'}), 201
    else:
        coffees = Coffee.query.all()
        return jsonify([{
            'id': c.id,
            'name': c.name,
            'price': c.price,
            'description': c.description,
            'image_url': c.image_url
        } for c in coffees])

@app.route('/api/menu/<int:id>', methods=['PUT', 'DELETE'])
def handle_menu_item(id):
    coffee = Coffee.query.get_or_404(id)

    if request.method == 'PUT':
        coffee.name = request.form['name']
        coffee.price = request.form['price']
        coffee.description = request.form.get('description', '')

        if 'image' in request.files and request.files['image'].filename != '':
            file = request.files['image']
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            coffee.image_url = f"/static/uploads/{filename}"

        db.session.commit()
        return jsonify({'message': 'Coffee updated successfully.'})

    elif request.method == 'DELETE':
        db.session.delete(coffee)
        db.session.commit()
        return jsonify({'message': 'Coffee deleted successfully.'})

# ---------------- Product Endpoints ----------------
@app.route('/api/products', methods=['GET', 'POST'])
def products():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        description = request.form.get('description', '')
        image_url = 'https://via.placeholder.com/150'

        if 'image' in request.files:
            file = request.files['image']
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            image_url = f"/static/uploads/{filename}"

        product = Product(name=name, price=price, description=description, image_url=image_url)
        db.session.add(product)
        db.session.commit()
        return jsonify({'message': 'Product added successfully'}), 201
    else:
        products = Product.query.all()
        return jsonify([{
            'id': p.id,
            'name': p.name,
            'price': p.price,
            'description': p.description,
            'image_url': p.image_url
        } for p in products])

@app.route('/api/products/<int:id>', methods=['PUT', 'DELETE'])
def handle_product_item(id):
    product = Product.query.get_or_404(id)

    if request.method == 'PUT':
        product.name = request.form['name']
        product.price = request.form['price']
        product.description = request.form.get('description', '')

        if 'image' in request.files and request.files['image'].filename != '':
            file = request.files['image']
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            product.image_url = f"/static/uploads/{filename}"

        db.session.commit()
        return jsonify({'message': 'Product updated successfully.'})

    elif request.method == 'DELETE':
        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': 'Product deleted successfully.'})

# ---------------- Cart Endpoints ----------------
@app.route('/api/cart', methods=['GET'])
def get_cart():
    items = CartItem.query.all()
    cart_data = []
    total = 0

    for item in items:
        if item.coffee:
            subtotal = item.coffee.price * item.quantity
            cart_data.append({
                'id': item.id,
                'type': 'coffee',
                'name': item.coffee.name,
                'price': item.coffee.price,
                'quantity': item.quantity,
                'image_url': item.coffee.image_url,
                'subtotal': subtotal
            })
            total += subtotal
        elif item.product:
            subtotal = item.product.price * item.quantity
            cart_data.append({
                'id': item.id,
                'type': 'product',
                'name': item.product.name,
                'price': item.product.price,
                'quantity': item.quantity,
                'image_url': item.product.image_url,
                'subtotal': subtotal
            })
            total += subtotal

    return jsonify({'items': cart_data, 'total': total})

@app.route('/api/cart', methods=['POST'])
def add_to_cart():
    try:
        data = request.get_json()
        print("Received cart data:", data)

        coffee_id = data.get('coffee_id')
        product_id = data.get('product_id')
        quantity = int(data.get('quantity', 1))

        if coffee_id:
            coffee = Coffee.query.get(coffee_id)
            if not coffee:
                return jsonify({'error': 'Coffee not found'}), 404

            existing = CartItem.query.filter_by(coffee_id=coffee_id, product_id=None).first()
            if existing:
                existing.quantity += quantity
            else:
                db.session.add(CartItem(coffee_id=coffee_id, quantity=quantity))

        elif product_id:
            product = Product.query.get(product_id)
            if not product:
                return jsonify({'error': 'Product not found'}), 404

            existing = CartItem.query.filter_by(product_id=product_id, coffee_id=None).first()
            if existing:
                existing.quantity += quantity
            else:
                db.session.add(CartItem(product_id=product_id, quantity=quantity))

        else:
            return jsonify({'error': 'No item ID provided'}), 400

        db.session.commit()
        return jsonify({'message': 'Item added to cart'})

    except Exception as e:
        print("Error adding to cart:", str(e))
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

# ---------------- Review Endpoints ----------------
@app.route('/api/reviews', methods=['GET', 'POST'])
def reviews():
    if request.method == 'POST':
        data = request.get_json()
        name = data.get('name')
        review_text = data.get('review')
        rating = data.get('rating')

        if not name or not review_text or not rating:
            return jsonify({'error': 'Missing required fields'}), 400

        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                return jsonify({'error': 'Rating must be between 1 and 5'}), 400
        except ValueError:
            return jsonify({'error': 'Invalid rating value'}), 400

        review = Review(name=name, review_text=review_text, rating=rating)
        db.session.add(review)
        db.session.commit()
        return jsonify({'message': 'Review added successfully'}), 201
    else:
        reviews = Review.query.order_by(Review.created_at.desc()).all()
        return jsonify([{
            'id': r.id,
            'name': r.name,
            'review_text': r.review_text,
            'rating': r.rating,
            'created_at': r.created_at.isoformat()
        } for r in reviews])

# ---------------- Checkout ----------------
@app.route('/api/checkout', methods=['POST'])
def checkout():
    CartItem.query.delete()
    db.session.commit()
    return jsonify({'message': 'Checkout successful and cart cleared.'})

# ---------------- Error Handlers ----------------
@app.errorhandler(400)
def bad_request_error(e):
    return jsonify({'error': 'Bad Request', 'details': str(e)}), 400

@app.errorhandler(404)
def not_found_error(e):
    return jsonify({'error': 'Not Found', 'details': str(e)}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500

# ---------------- Run App ----------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5001)
