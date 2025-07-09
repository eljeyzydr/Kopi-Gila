from flask import Flask, render_template
import os

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/review')
def review():
    return render_template('review.html')

@app.route('/products')
def products():
    return render_template('products.html')

@app.route('/contacts')
def contacts():
    return render_template('contacts.html')

@app.route('/blogs')
def blogs():
    return render_template('blogs.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)