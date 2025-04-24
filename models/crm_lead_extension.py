from odoo import models, api, exceptions
import logging

_logger = logging.getLogger(__name__)


class CRMLead(models.Model):
    _inherit = 'crm.lead'
    """
    def action_sale_quotations_new(self):
        _logger.warning("action_sale_quotations_new")
        if self.partner_id: 
            if not self.partner_id.vat:
                raise exceptions.UserError(
                    "No se puede crear un presupuesto porque el cliente no tiene el campo (CUIT/CUIL/DNI) completo."
                )
            #elif not self.partner_id.email:
            #    raise exceptions.UserError(
            #        "No se puede crear un presupuesto porque el cliente no tiene el campo (Correo electrónico) completo."
            #   )
        return super(CRMLead, self).action_sale_quotations_new()
    
    """