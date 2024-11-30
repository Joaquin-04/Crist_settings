from odoo import models, fields, api

class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.model_create_multi
    def create(self, vals_list):
        # For each move being created, set the quantity to 0
        for vals in vals_list:
            vals['quantity'] = 0
        return super(StockMove, self).create(vals_list)
