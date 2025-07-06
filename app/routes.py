from flask import Blueprint, render_template, session, request, redirect, url_for, flash

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/menu', methods=['GET', 'POST'])
def menu():
    if 'cart' not in session:
        session['cart'] = []
    if request.method == 'POST':
        item = request.form.get('item')
        quantity = int(request.form.get('quantity', 1))
        if item:
            for _ in range(quantity):
                session['cart'].append(item)
            session.modified = True
    return render_template('menu.html')

@main.route('/cart', methods=['GET', 'POST'])
def cart():
    cart = session.get('cart', [])
    message = None
    if request.method == 'POST':
        seat = request.form.get('seat')
        # Simpan data ke database jika diperlukan
        message = f"Pesanan Anda untuk kursi {seat} telah dikonfirmasi!"
        session.pop('cart', None)
    return render_template('cart.html', cart=cart, message=message)

@main.route('/products')
def products():
    return render_template('products.html')

@main.route('/review')
def review():
    return render_template('review.html')

@main.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        # TODO: Simpan ke database atau kirim via email
        flash('Pesan Anda telah dikirim. Terima kasih!', 'success')
        return redirect(url_for('main.contact'))
    return render_template('contact.html')


@main.route('/blogs')
def blogs():
    return render_template('blogs.html')
