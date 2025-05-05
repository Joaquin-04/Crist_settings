from odoo import models, api, fields
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # Campos - Atributos del Producto
    nv_tipo = fields.Many2one(
        "project.obratipo", 
        string="NV Tipo",
        tracking=True
    )
    nv_linea = fields.Many2one(
        "project.lnarti", 
        string="NV Línea",
        tracking=True
    )
    nv_color = fields.Many2one(
        "project.color", 
        string="NV Color",
        tracking=True
    )
    nv_cantidad_carpinteria = fields.Char(
        string="NV Cantidad de Carpintería",
        tracking=True
    )
    nv_es_express = fields.Boolean(
        string="NV ¿Es Express?",
        tracking=True
    )

    # Campos - Unidades
    nv_kg_perfileria = fields.Integer(
        string="NV Kg Perfilería",
        tracking=True
    )
    nv_m2_producto_terminado = fields.Float(
        string="NV M2 Producto Terminado",
        tracking=True
    )
    nv_lleva_dvh = fields.Boolean(
        string="NV ¿Lleva DVH?",
        tracking=True
    )

    #Modificando el compute del display_name, par que combine el nombre del cliente con el nombre de la orden de venta.
    @api.depends('name', 'partner_id.name')
    def _compute_display_name(self):
        for order in self:
            if order.opportunity_id:
                order.display_name = f"{order.opportunity_id.name} - {order.name}"
            else:
                order.display_name = order.name

    # Funcion que sirve para abrir una ventana con la oportunidad relacionada con la orden de venta
    # esta accion va a ser llamada por un boton en la vista form de la orden de venta.
    def action_open_opportunity(self):
        self.ensure_one()  # Asegura que se trabaja con un único registro
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'crm.lead',  # Modelo de la oportunidad (crm.lead)
            'res_id': self.opportunity_id.id,  # ID de la oportunidad relacionada
            'views': [(False, 'form')],  # Vista de formulario
            'view_mode': 'form',
            'target': 'current',  # Abre en la misma ventana
        }
    
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


