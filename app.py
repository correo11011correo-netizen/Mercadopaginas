# -*- coding: utf-8 -*-
"""
Servidor web principal para la aplicación Mercadopaginas.

Este archivo inicializa la aplicación Flask y define las rutas
para servir las páginas principales y las demos.
"""
import os
from datetime import datetime
from flask import Flask, render_template, send_from_directory, abort

app = Flask(__name__)

# --- Datos de Ejemplo ---
# En una aplicación real, estos datos vendrían de una base de datos.
WEBSITE_DATA = {
    'categories': [
        {
            'id': 1,
            'name': 'Automóviles',
            'websites': [
                {'id': 1, 'name': 'Blog de Autos', 'description': 'Un blog para entusiastas de los coches.', 'price': 100, 'demo_url': 'auto-blog/index'},
                {'id': 2, 'name': 'Clasificados de Autos', 'description': 'Compra y vende coches usados.', 'price': 150, 'demo_url': 'auto-clasificados/index'},
            ]
        },
        {
            'id': 2,
            'name': 'Inmobiliaria',
            'websites': [
                {'id': 3, 'name': 'Agente Inmobiliario', 'description': 'Sitio web para agentes de bienes raíces.', 'price': 120, 'demo_url': 'inmo-agente/index'},
                {'id': 4, 'name': 'Propiedades de Lujo', 'description': 'Catálogo de propiedades exclusivas.', 'price': 200, 'demo_url': 'inmo-pro/index'},
            ]
        },
        {
            'id': 3,
            'name': 'Tiendas',
            'websites': [
                {'id': 5, 'name': 'Tienda de Barrio', 'description': 'E-commerce para pequeños negocios.', 'price': 180, 'demo_url': 'tienda-barrio/index'},
                {'id': 6, 'name': 'Boutique de Ropa', 'description': 'Tienda online para marcas de moda.', 'price': 250, 'demo_url': 'ropa-boutique/index'},
            ]
        }
    ]
}

@app.context_processor
def inject_current_year():
    """ Inyecta el año actual en todas las plantillas. """
    return {'current_year': datetime.utcnow().year}

@app.route('/')
def index():
    """
    Renderiza la página principal con los datos del catálogo.
    """
    categories = WEBSITE_DATA['categories']
    return render_template('index.html', categories=categories)

@app.route('/demos/<path:filename>')
def demo(filename):
    """
    Sirve los archivos HTML estáticos de las demos de forma segura.
    """
    # Directorio base donde se encuentran las demos
    demo_dir = os.path.join(app.root_path, 'templates', 'demos')
    
    # send_from_directory maneja la seguridad contra path traversal
    return send_from_directory(demo_dir, filename + '.html')

if __name__ == '__main__':
    # Esta sección solo se ejecuta al correr el script directamente (ej. `python app.py`)
    # Es útil para desarrollo local, pero no debe ejecutarse en producción con mod_wsgi.
    app.run(debug=True, port=5000)
