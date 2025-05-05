{
    'name': 'Custom Crist Configurations',
    'version': '1.0',
    'summary': 'Configuraciones específicas para la empresa',
    'author': 'Tu Empresa',
    'depends': ['project','Project_Custom','crm','sale_management', 'purchase', 'stock'],
    'data': [
        'views/sale_order_views.xml',
    ],
    'post_init_hook': 'post_init_hook',
    'installable': True,
    'application': False,
}
