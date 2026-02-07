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
                {'id': 1, 'name': 'Blog de Autos', 'description': 'Un blog moderno y dinámico para entusiastas de los coches, con reseñas, noticias y guías.', 'price': 125, 'demo_url': 'auto-blog/index', 'image_id': 'auto-blog'},
                {'id': 2, 'name': 'Clasificados de Autos', 'description': 'Plataforma completa para comprar y vender coches usados, con filtros y perfiles de usuario.', 'price': 170, 'demo_url': 'auto-clasificados/index', 'image_id': 'auto-clasificados'},
                {'id': 7, 'name': 'Taller Mecánico', 'description': 'Web profesional para talleres, ideal para mostrar servicios, horarios y agendar citas online.', 'price': 150, 'demo_url': 'auto-taller/index', 'image_id': 'auto-taller'},
            ]
        },
        {
            'id': 2,
            'name': 'Inmobiliaria',
            'websites': [
                {'id': 3, 'name': 'Agente Inmobiliario', 'description': 'Sitio web personal para agentes, perfecto para destacar propiedades y captar nuevos clientes.', 'price': 140, 'demo_url': 'inmo-agente/index', 'image_id': 'inmo-agente'},
                {'id': 4, 'name': 'Propiedades de Lujo', 'description': 'Catálogo online de alta gama para propiedades exclusivas, con galerías de fotos y mapas.', 'price': 220, 'demo_url': 'inmo-pro/index', 'image_id': 'inmo-pro'},
                {'id': 8, 'name': 'Alquiler Vacacional', 'description': 'Página de aterrizaje atractiva para promocionar y reservar propiedades de alquiler turístico.', 'price': 160, 'demo_url': 'inmo-vacacional/index', 'image_id': 'inmo-vacacional'},
            ]
        },
        {
            'id': 3,
            'name': 'Tiendas',
            'websites': [
                {'id': 5, 'name': 'Tienda de Barrio', 'description': 'E-commerce funcional para pequeños negocios que quieran vender sus productos en línea.', 'price': 190, 'demo_url': 'tienda-barrio/index', 'image_id': 'tienda-barrio'},
                {'id': 6, 'name': 'Boutique de Ropa', 'description': 'Tienda online elegante para marcas de moda, con enfoque en el producto y la estética visual.', 'price': 260, 'demo_url': 'ropa-boutique/index', 'image_id': 'ropa-boutique'},
                {'id': 9, 'name': 'Blog de Moda', 'description': 'Un espacio para crear contenido, mostrar tendencias y construir una comunidad de seguidores.', 'price': 130, 'demo_url': 'ropa-blog/index', 'image_id': 'ropa-blog'},
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
