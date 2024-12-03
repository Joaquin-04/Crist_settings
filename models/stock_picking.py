from odoo import models, api
from odoo.exceptions import UserError

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        for picking in self:
            partner = picking.partner_id
            if not partner.l10n_latam_identification_type_id or not partner.vat:
                raise UserError("El contacto debe tener configurado el tipo de identificación y el campo (CUIT/CUIL/DNI) completo para validar el remito.")
            elif not partner.email:
                raise UserError(
                    "No se puede crear un presupuesto porque el cliente no tiene el campo (Correo electrónico) completo."
                )
        return super(StockPicking, self).button_validate()
