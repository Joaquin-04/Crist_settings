from odoo import models, api
from odoo.exceptions import UserError

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def button_confirm(self):
        for order in self:
            partner = order.partner_id
            if not partner.l10n_latam_identification_type_id or not partner.vat:
                raise UserError("El contacto debe tener configurado el tipo de identificación y el VAT para confirmar la orden de compra.")
        return super(PurchaseOrder, self).button_confirm()
