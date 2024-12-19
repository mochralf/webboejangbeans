from flask_session import Session
from flask import Flask, render_template, redirect, request, session, jsonify, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime
import mysql.connector
from flask import url_for
from werkzeug.security import generate_password_hash, check_password_hash
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = 'kopi123' 
app.config['SESSION_TYPE'] = 'filesystem'  
app.config['SESSION_PERMANENT'] = False
Session(app)

# Flask-Login Setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

db_config = {
    user="webboejangbeans", 
    password="Admin123",
    host="webboejangbeans.mysql.database.azure.com", 
    port=3306, 
    database="boejangbeans"
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

# User class untuk Flask-Login
class User(UserMixin):
    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email

@login_manager.user_loader
def load_user(user_id):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT id, username, email FROM account WHERE id = %s", (user_id,))
    user_data = cursor.fetchone()
    cursor.close()
    connection.close()

    if user_data:
        return User(user_data["id"], user_data["username"], user_data["email"])
    return None

@app.before_request
def before_request():
    if 'cart' not in session:
        session['cart'] = []

        
@app.route('/')
@login_required
def index():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT id, nama, harga, stok, foto, typeCoffee FROM product")
    products = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('index.html', products=products)


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = request.form.get('id')
    product_name = request.form.get('nama')
    product_price = request.form.get('harga')
    product_image = request.form.get('foto')

    if 'cart' not in session:
        session['cart'] = []

    if not product_id:
        flash("Produk tidak valid!", "error")
        return redirect(url_for('index'))
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT id, nama, harga, foto FROM product WHERE id = %s", (product_id,))
    product = cursor.fetchone()
    cursor.close()
    connection.close()

    if not product:
        flash("Produk tidak ditemukan!", "error")
        return redirect(url_for('index'))

    if 'cart' not in session or not isinstance(session['cart'], list):
        session['cart'] = []
    print("Product to add:", product)

    for item in session['cart']:
        if item.get('id') == product['id']:
            item['quantity'] += 1
            break
    else:
        session['cart'].append({
            'id': product['id'],  
            'name': product['nama'],
            'price': product['harga'],
            'image': product['foto'],
            'quantity': 1
        })

    session.modified = True
    flash("Produk berhasil ditambahkan ke keranjang!", "success")
    return redirect(url_for('trolley'))



@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    print("Cart before removing:", session.get('cart', []))
    print("Product ID to remove:", request.form.get('product_id'))

    if 'cart' in session and isinstance(session['cart'], list):
        product_id = request.form.get('product_id')

        if product_id:
            for item in session['cart']:
                print("Item in cart:", item)
            try:
                session['cart'] = [
                    item for item in session['cart'] if str(item.get('id')) != str(product_id)
                ]
                session.modified = True
                flash("Produk berhasil dihapus dari keranjang!", "success")
            except KeyError as e:
                flash(f"Kesalahan: {e}", "error")
        else:
            flash("Produk tidak valid!", "error")
    else:
        flash("Keranjang kosong atau tidak valid!", "error")

    return redirect(url_for('trolley'))


@app.route('/trolley')
def trolley():
    cart = session.get('cart', [])
    print("Current Cart:", cart)  

    total_price = sum(
        int(product['price']) * product['quantity']
        for product in cart
        if product.get('price') is not None and product.get('quantity') is not None
    )

    return render_template('trolley.html', cart=cart, total_price=total_price)


@app.route('/filter/', methods=['GET'])
def filter():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    product = []
    if request.args.get('typeCoffee'):
        query = request.args.get('typeCoffee')
        cursor.execute("SELECT id, nama, harga, stok, foto, typeCoffee FROM product WHERE typeCoffee = %s ORDER BY nama ASC", (query,))
        product = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('index.html', products=product)


@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart = session.get('cart', [])
    print("Current Cart:", cart)
    total_price = sum(
        int(item['price']) * item['quantity']
        for item in cart
        if item.get('price') is not None and item.get('quantity') is not None
    )

    user_name = current_user.username
    user_email = current_user.email

    if request.method == 'POST':
        payment_method = request.form['payment_method']
        print("Payment Method:", payment_method)  # Tambahkan print untuk debug
        address = request.form['address']
        phone_number = request.form['no_hp']
        
        connection = get_db_connection()
        cursor = connection.cursor()
        for product in cart:
            item_price = float(product['price'])  # Pastikan price adalah float
            item_quantity = int(product['quantity'])  # Pastikan quantity adalah integer
            total_item_price = item_price * item_quantity
            
            cursor.execute("""
                INSERT INTO purchases (
                    user_id, product_id, quantity, total_price, payment_method, email, address, phone_number
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                current_user.id,         
                product['id'],            
                product['quantity'],      
                total_item_price,         
                payment_method,           
                user_email,                
                address,
                phone_number
            ))
            print(f"Inserted Payment Method: {payment_method}")
        connection.commit()
        cursor.close()
        connection.close()

        flash('Pembelian berhasil dilakukan!', 'success')
        session['cart'] = []  
        return redirect(url_for('checkout'))

    return render_template(
        'checkout.html',
        cart_items=cart,
        total_price=total_price,
        user_name=user_name,
        user_email=user_email
    )


@app.route("/contact", methods=["POST"])
def contact():
    if request.method == "POST":
        nama = request.form["nama"]
        email = request.form["email"]
        no_hp = request.form["no_hp"]
        pesan = request.form["pesan"]

        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        sql = "INSERT INTO contact (nama, email, no_hp, pesan) VALUES (%s, %s, %s, %s)"
        values = (nama, email, no_hp, pesan)
        cursor.execute(sql, values)
        connection.commit()

        cursor.close()
        connection.close()

    return render_template("index.html")

# Berkaitan dengan Admin dan Dashboardnya !!!
admin_credentials = {
    'username': 'admin',
    'password': 'kopi123'
}

def admin_login_required(f):
    """Dekorator untuk memeriksa apakah admin sudah login."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "username" not in session or session["username"] != admin_credentials['username']:
            flash("Silakan login terlebih dahulu untuk mengakses halaman ini.", "error")
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == admin_credentials['username'] and password == admin_credentials['password']:
            session["username"] = username  # Set sesi admin
            flash("Berhasil login sebagai admin.", "success")
            return redirect(url_for("admin_dashboard"))
        else:
            error = "Username atau password salah."
            return render_template("admin.html", error=error)

    return render_template("admin.html")

@app.route("/admin_dashboard")
@admin_login_required  # Pastikan admin login sebelum mengakses dashboard
def admin_dashboard():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM contact")
    contacts = cursor.fetchall()

    cursor.execute("SELECT * FROM product")
    products = cursor.fetchall()

    cursor.execute("SELECT * FROM account")
    accounts = cursor.fetchall()

    cursor.execute("SELECT * FROM purchases")
    purchases = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "admin_dashboard.html",
        contacts=contacts,
        products=products,
        accounts=accounts,
        purchases=purchases
    )

@app.route("/admin_logout")
def admin_logout():
    """Route untuk logout admin."""
    session.pop("username", None)  # Hapus sesi admin
    flash("Anda telah logout.", "success")
    return redirect(url_for("admin_login"))

# Berkaitan dengan Akun !!!
@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        # Ambil hash password dan salt dari database
        sql = "SELECT id, username, password_hash, salt FROM account WHERE username = %s"
        cursor.execute(sql, (username,))
        user = cursor.fetchone()

        cursor.close()
        connection.close()

        if user:
            salted_password = password + user["salt"]  
            if check_password_hash(user["password_hash"], salted_password): 
                user_obj = User(user["id"], user["username"], user.get("email", None))
                login_user(user_obj) 
                return redirect(url_for("index"))  
            else:
                error = "Password salah."
        else:
            error = "Username tidak ditemukan."

        return render_template("login.html", error=error)

    return render_template("login.html")

@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/logged/", methods=["POST"] )
def logged():
    # Get log in info from log in form
    user = request.form["username"].lower()
    pwd = request.form["password"]
    #pwd = str(sha1(request.form["password"].encode('utf-8')).hexdigest())
    # Make sure form input is not blank and re-render log in page if blank
    if user == "" or pwd == "":
        return render_template ( "login.html" )
    # Find out if info in form matches a record in user database
    query = "SELECT * FROM account WHERE username = :user AND password_hash = :pwd"
    rows = mysql.connection.cursor ( query, user=user, pwd=pwd )

    # If username and password match a record in database, set session variables
    if len(rows) == 1:
        session['user'] = user
        session['time'] = datetime.now( )
        session['uid'] = rows[0]["id"]
    # Redirect to Home Page
    if 'user' in session:
        return redirect ( "/" )
    # If username is not in the database return the log in page
    return render_template ( "login.html", msg="Wrong username or password." )



@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        fname = request.form["fname"]
        lname = request.form["lname"]
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        # Generate a unique salt
        salt = os.urandom(16).hex()  # Generates a 32-character hexadecimal string
        salted_password = password + salt  # Combine password and salt

        # Hash the salted password
        password_hash = generate_password_hash(salted_password)

        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        try:
            sql = """
                INSERT INTO account (fname, lname, username, email, password_hash, salt)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (fname, lname, username, email, password_hash, salt)
            cursor.execute(sql, values)
            connection.commit()
            success_message = "Pendaftaran berhasil! Silakan login."
            return render_template("login.html", success_message=success_message)
        except mysql.connector.Error as err:
            error_message = f"Terjadi kesalahan: {err}"
            return render_template("register.html", error_message=error_message)
        finally:
            cursor.close()
            connection.close()
    return render_template("register.html")

@app.route('/resetpasswd')
def resetpasswd():
    return render_template('respasswd.html')




# Berkaitan dengan CRUD !!!
@app.route("/add_contact", methods=["GET", "POST"])
def add_contact():
    if request.method == "POST":
        nama = request.form["nama"]
        email = request.form["email"]
        no_hp = request.form["no_hp"]
        pesan = request.form["pesan"]

        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        sql = "INSERT INTO contact (nama, email, no_hp, pesan) VALUES (%s, %s, %s, %s)"
        values = (nama, email, no_hp, pesan)
        cursor.execute(sql, values)
        connection.commit()

        cursor.close()
        connection.close()

        return redirect(url_for("admin_dashboard"))

    return render_template("add_contact.html")

@app.route("/update_contact/<int:id>", methods=["GET", "POST"])
def update_contact(id):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    if request.method == "POST":
        nama = request.form["nama"]
        email = request.form["email"]
        no_hp = request.form["no_hp"]
        pesan = request.form["pesan"]

        sql = "UPDATE contact SET nama = %s, email = %s, no_hp = %s, pesan = %s WHERE id = %s"
        values = (nama, email, no_hp, pesan, id)
        cursor.execute(sql, values)
        connection.commit()

        cursor.close()
        connection.close()

        return redirect(url_for("admin_dashboard"))

    cursor.execute("SELECT * FROM contact WHERE id = %s", (id,))
    contact = cursor.fetchone()

    cursor.close()
    connection.close()

    return render_template("update_contact.html", contact=contact)

@app.route("/delete/<int:id>")
def delete_contact(id):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    cursor.execute("DELETE FROM contact WHERE id = %s", (id,))
    connection.commit()

    cursor.close()
    connection.close()

    return redirect(url_for("admin_dashboard"))

@app.route("/add_product", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        nama = request.form["nama"]
        harga = request.form["harga"]
        stok = request.form["stok"]
        foto = request.form["foto"]
        typeCoffee = request.form["typeCoffee"]

        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        sql = "INSERT INTO product (nama, harga, stok, foto, typeCoffee) VALUES (%s, %s, %s, %s, %s)"
        values = (nama, harga, stok, foto, typeCoffee)
        cursor.execute(sql, values)
        connection.commit()

        cursor.close()
        connection.close()

        return redirect(url_for("admin_dashboard"))

    return render_template("add_product.html")

@app.route("/update_product/<int:id>", methods=["GET", "POST"])
def update_product(id):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    if request.method == "POST":
        nama = request.form["nama"]
        harga = request.form["harga"]
        stok = request.form["stok"]

        sql = "UPDATE product SET nama = %s, harga = %s, stok = %s WHERE id = %s"
        values = (nama, harga, stok, id)
        cursor.execute(sql, values)
        connection.commit()

        cursor.close()
        connection.close()

        return redirect(url_for("admin_dashboard"))

    cursor.execute("SELECT * FROM product WHERE id = %s", (id,))
    product = cursor.fetchone()

    cursor.close()
    connection.close()

    return render_template("update_product.html", product=product)

@app.route("/delete_product/<int:id>")
def delete_product(id):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    cursor.execute("DELETE FROM product WHERE id = %s", (id,))
    connection.commit()

    cursor.close()
    connection.close()

    return redirect(url_for("admin_dashboard"))

@app.route("/add_account", methods=["GET", "POST"])
def add_account():
    if request.method == "POST":
        fname = request.form["fname"]
        lname = request.form["lname"]
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        password_hash = generate_password_hash(password)
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        sql = "INSERT INTO account (fname, lname, username, email, password_hash) VALUES (%s, %s, %s, %s, %s)"
        values = (fname, lname, username, email, password_hash)
        cursor.execute(sql, values)
        connection.commit()

        cursor.close()
        connection.close()

        return redirect(url_for("admin_dashboard"))

    return render_template("add_account.html")

@app.route("/delete_account/<int:id>")
def delete_account(id):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    cursor.execute("DELETE FROM account WHERE id = %s", (id,))
    connection.commit()

    cursor.close()
    connection.close()

    return redirect(url_for("admin_dashboard"))

@app.route("/delete_purchases/<int:id>")
def delete_purchases(id):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    cursor.execute("DELETE FROM purchases WHERE id = %s", (id,))
    connection.commit()

    cursor.close()
    connection.close()

    return redirect(url_for("admin_dashboard"))

@app.route('/Rafli Profile')
def rafli():
    return render_template('rafli.html')

@app.route('/Nagita Profile')
def nagita():
    return render_template('nagita.html')

@app.route('/Azzam Profile')
def azzam():
    return render_template('azzam.html')

@app.route('/Faqih Profile')
def faqih():
    return render_template('faqih.html')



if __name__ == "__main__":
    app.run()
