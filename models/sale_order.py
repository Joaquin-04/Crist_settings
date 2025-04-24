from odoo import models, api
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    #Modificando el compute del display_name, par que combine el nombre del cliente con el nombre de la orden de venta.

    @api.depends('name', 'partner_id.name')
    def _compute_display_name(self):
        for order in self:
            if order.partner_id:
                order.display_name = f"{order.partner_id.name} - {order.name}"
            else:
                order.display_name = order.name

    
    def action_confirm(self):
        for order in self:
            partner = order.partner_id
            if not partner.l10n_latam_identification_type_id or not partner.vat:
                raise UserError("El contacto debe tener configurado el tipo de identificación y el campo (CUIT/CUIL/DNI) completo para confirmar la orden de venta.")
            #elif not partner.email:
            #    raise UserError(
            #        "No se puede crear un presupuesto porque el cliente no tiene el campo (Correo electrónico) completo."
            #    )
        return super(SaleOrder, self).action_confirm()

    
    @api.onchange('opportunity_id')
    def _onchange_opportunity_id(self):
        """Metodo para heredar datos de la oportunidad """
        if self.opportunity_id: 
            if self.opportunity_id.x_studio_nv_numero_de_obra_relacionada:
                self.x_studio_nv_numero_de_obra_relacionada = self.opportunity_id.x_studio_nv_numero_de_obra_relacionada
            if self.opportunity_id.x_studio_nv_numero_de_sp:
                self.x_studio_nv_numero_de_obra_padre = self.opportunity_id.x_studio_nv_numero_de_sp


