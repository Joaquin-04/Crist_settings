from odoo import models, api, exceptions, _
import logging
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class CRMLead(models.Model):
    _inherit = 'crm.lead'

    # Lista de campos obligatorios para el estado 1210
    REQUIRED_FIELDS_STATE_1210 = [
        'partner_id',
        'project_ubi_id',
        'provincia_id',
        'obratipo_proyect_id',
        'lnart_proyect_id',
        'color_proyect_id',
        'color_proyect_id',
    ]

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


    def write(self, vals):
        if 'stage_id' in vals:
            stage_1210 = self.env['crm.stage'].browse(vals['stage_id'])
            if stage_1210.id == 20:  # ID de la etapa "Cotizar"
                error_messages = []
                
                for lead in self:
                    # Combinar valores actuales con los nuevos
                    combined_vals = lead.copy_data()[0]
                    combined_vals.update(vals)
                    
                    # Verificar campos faltantes
                    missing = [
                        field for field in self.REQUIRED_FIELDS_STATE_1210
                        if not combined_vals.get(field)
                    ]
                    
                    if missing:
                        # Obtener nombres de campos
                        field_names = lead.fields_get(missing)
                        pretty_names = [
                            field_names[f]['string'] for f in missing
                        ]
                        for name in pretty_names:
                            error_messages.append(
                                f"⛔ {name}"
                            )
                
                if error_messages:
                    raise ValidationError(_(
                        "¡Campos requeridos faltantes!\n\n%s\n\n"
                        "Complete los campos antes de cambiar al estado 'Cotizar'"
                    ) % "\n".join(error_messages))

        # === Actualizar vendedor en cotizaciones y facturas si cambia user_id ===
        if 'user_id' in vals:
            for lead in self:
                # Actualizar vendedor en cotizaciones
                quotations = self.env['sale.order'].search([('opportunity_id', '=', lead.id)])
                quotations.write({'user_id': vals['user_id']})
    
                # Actualizar vendedor en facturas relacionadas
                invoices = self.env['account.move'].search([
                    ('invoice_origin', 'in', quotations.mapped('name')),
                    ('move_type', '=', 'out_invoice')  # Facturas de cliente
                ])
                invoices.write({'user_id': vals['user_id']})
    
                _logger.info(f"[CRMLead] user_id actualizado a {vals['user_id']} en {len(quotations)} cotizaciones y {len(invoices)} facturas (lead ID: {lead.id})")
    
        return super(CRMLead, self).write(vals)


    def _prepare_invoice(self):
        invoice_vals = super()._prepare_invoice()
        if self.user_id:
            invoice_vals['user_id'] = self.user_id.id
        return invoice_vals








        