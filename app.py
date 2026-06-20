from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    'sqlite:///productos.db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# MODELO

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)

# CREAR TABLAS

with app.app_context():
    db.create_all()

# RUTA PRINCIPAL

@app.route('/')
def index():
    productos = Producto.query.all()
    return render_template('index.html', productos=productos)

# CREAR

@app.route('/crear', methods=['GET', 'POST'])
def crear():

    if request.method == 'POST':

        nombre = request.form['nombre']
        precio = float(request.form['precio'])
        stock = int(request.form['stock'])

        nuevo = Producto(
            nombre=nombre,
            precio=precio,
            stock=stock
        )

        db.session.add(nuevo)
        db.session.commit()

        return redirect('/')

    return render_template('crear.html')

# EDITAR

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):

    producto = Producto.query.get_or_404(id)

    if request.method == 'POST':

        producto.nombre = request.form['nombre']
        producto.precio = float(request.form['precio'])
        producto.stock = int(request.form['stock'])

        db.session.commit()

        return redirect('/')

    return render_template(
        'editar.html',
        producto=producto
    )

# ELIMINAR

@app.route('/eliminar/<int:id>')
def eliminar(id):

    producto = Producto.query.get_or_404(id)

    db.session.delete(producto)
    db.session.commit()

    return redirect('/')

# EJECUTAR APP

if __name__ == '__main__':
    app.run(debug=True)