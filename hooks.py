from odoo import api, SUPERUSER_ID

def post_init_hook(cr, registry):
    """ 
    Recalcula el campo `display_name` para todas las órdenes existentes 
    al instalar el módulo.
    """
    env = api.Environment(cr, SUPERUSER_ID, {})
    sale_orders = env['sale.order'].search([])
    sale_orders._compute_display_name()  # Fuerza el cálculo