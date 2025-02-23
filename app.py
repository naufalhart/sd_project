from flask import Flask, request, redirect, url_for, render_template, session, flash
from functools import wraps
import json
from slugify import slugify  # pip install python-slugify

app = Flask(__name__)
app.secret_key = 'feaaefafaefafasgwg3543t3w3tw43'

def load_products():
    with open('data/data.json', 'r') as file:
        return json.load(file)

@app.route('/')
def index():
    products = load_products()

    # Ambil parameter kategori dari URL
    category = request.args.get('category', 'all')  # Default: tampilkan semua
    sort_by = request.args.get('sort_by', 'default')

    # Konversi dictionary ke list agar bisa diurutkan dan difilter
    products_list = list(products.items())

    # Filter berdasarkan kategori jika bukan 'all'
    if category != 'all':
        products_list = [item for item in products_list if item[1]['category'] == category]

    # Sorting berdasarkan parameter (opsional)
    if sort_by == 'name_asc':
        products_list.sort(key=lambda x: x[0].lower())  # Urutkan nama A-Z
    elif sort_by == 'name_desc':
        products_list.sort(key=lambda x: x[0].lower(), reverse=True)  # Urutkan nama Z-A
    elif sort_by == 'price_low':
        products_list.sort(key=lambda x: x[1]['price'])  # Urutkan harga termurah
    elif sort_by == 'price_high':
        products_list.sort(key=lambda x: x[1]['price'], reverse=True)  # Urutkan harga termahal

    # Konversi kembali ke dictionary untuk template
    sorted_products = dict(products_list)

    return render_template('index.html', products=sorted_products, category=category, sort_by=sort_by)


@app.route('/product/<slug>')
def product_detail(slug):
    products = load_products()
    # Cari produk berdasarkan slug
    for name, details in products.items():
        if slugify(name) == slug:
            return render_template('product.html', 
                                 name=name, 
                                 details=details,
                                 slugify=slugify)
    return render_template('error.html', message="404 Product Not Found!")

# Filter kustom untuk generate slug
@app.template_filter('slugify')
def slugify_filter(s):
    return slugify(s)

@app.route('/search')
def search():
    query = request.args.get('q', '').lower()
    if not query:
        return redirect(url_for('index'))
        
    products = load_products()
    
    # Filter produk berdasarkan query
    search_results = {
        name: details for name, details in products.items()
        if query in name.lower() or 
        any(query in color.lower() for color in details.get('colors', []))
    }
    
    return render_template('search_results.html', 
                         query=query, 
                         products=search_results)

# Model untuk item keranjang (bisa disimpan di database)
class CartItem:
    def __init__(self, product_id, name, price, quantity=1):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity

# Route untuk menambahkan ke keranjang
@app.route('/add-to-cart/<product_id>', methods=['POST'])
def add_to_cart(product_id):
    products = load_products()  # Load your products data
    
    # Inisialisasi keranjang jika belum ada
    if 'cart' not in session:
        session['cart'] = {}
    
    # Cari produk berdasarkan ID
    product = None
    for name, details in products.items():
        if slugify(name) == product_id:
            product = {'name': name, 'details': details}
            break
    
    if product:
        cart = session['cart']
        if product_id in cart:
            # Jika produk sudah ada, tambah quantity
            cart[product_id]['quantity'] += 1
        else:
            # Jika produk belum ada, tambahkan ke keranjang
            # Pastikan menggunakan key yang benar sesuai data produk Anda
            cart[product_id] = {
                'name': product['name'],
                'price': product['details']['price'],
                'quantity': 1,
                'image': product['details'].get('image', '')  # Gunakan .get() dengan nilai default
                # atau sesuaikan dengan struktur data produk Anda:
                # 'image': product['details']['gambar'] # jika key-nya 'gambar'
                # 'image': product['details']['foto']   # jika key-nya 'foto'
            }
            
        session.modified = True
        flash('Produk berhasil ditambahkan ke keranjang!', 'success')
        return redirect(url_for('product_detail', slug=product_id))
    
    flash('Produk tidak ditemukan', 'error')
    return redirect(url_for('product_detail', slug=product_id))


# Route untuk melihat keranjang
@app.route('/cart')
def cart():
    cart = session.get('cart', {})  # Jika tidak ada, set sebagai dictionary kosong

    if not cart:  # Jika keranjang kosong
        return render_template('cart.html', cart={}, total=0)

    total = 0
    for item in cart.values():
        try:
            item['price'] = int(str(item['price']).replace('.', '').strip())  # Konversi harga jadi integer
            item['quantity'] = int(item.get('quantity', 1))  # Pastikan quantity adalah integer
            total += item['price'] * item['quantity']
        except ValueError:
            item['price'] = 0  # Jika ada kesalahan, set harga ke 0

    return render_template('cart.html', cart=cart, total=total)


# Route untuk mengupdate quantity
@app.route('/update-cart/<product_id>', methods=['POST'])
def update_cart(product_id):
    quantity = int(request.form.get('quantity', 1))
    if 'cart' in session and product_id in session['cart']:
        if quantity > 0:
            session['cart'][product_id]['quantity'] = quantity
        else:
            del session['cart'][product_id]
        session.modified = True
    return redirect(url_for('cart'))

# Route untuk menghapus item dari keranjang
@app.route('/remove-from-cart/<product_id>')
def remove_from_cart(product_id):
    if 'cart' in session and product_id in session['cart']:
        del session['cart'][product_id]
        session.modified = True
    return redirect(url_for('cart'))

@app.route('/products')
def product_list():
    return render_template('products.html')

if __name__ == '__main__':
    app.run(debug=True)