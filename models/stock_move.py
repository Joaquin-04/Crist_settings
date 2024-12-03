from odoo import models, fields, api

import logging

_logger = logging.getLogger(__name__)

class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.model_create_multi
    def create(self, vals_list):
        _logger.warning(f"vals_list {vals_list}")
        # For each move being created, set the quantity to 0
        if 'is_inventory'in vals_list and not vals_list[0]['is_inventory']:
            for vals in vals_list:
                vals['quantity'] = 0
        return super(StockMove, self).create(vals_list)
