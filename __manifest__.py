{
    'name': 'Alquiler de productos',
    'version': '1.0',
    'summary': 'Módulo para gestionar el alquiler de productos',
    'category': 'Custom',
    'author': 'David Márquez Pozo',
    'website': 'https://tuweb.com',
    'license': 'LGPL-3',
    'depends': ['base', 'product', 'sale'],
    'icon': '/alquiler_producto/static/description/icon57.png',
    'data': [
        'data/alquiler_cron.xml',
        'views/alquiler_producto_views.xml',
        'security/ir.model.access.csv',
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
    'description': """
Módulo de Odoo para la gestión de alquileres de productos.
"""
}