from odoo import models, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class MergePartnerAutomatic(models.TransientModel):
    _inherit = 'base.partner.merge.automatic.wizard'

    def _merge(self, partner_ids, dst_partner=None, extra_checks=True):
        _logger.warning("Entrando al _merge")
        """
        Sobrescribe el método para permitir la fusión de contactos sin validar el correo electrónico,
        independientemente del usuario que ejecute la acción.
        """
        # Forzar `extra_checks` a False para evitar la validación del correo electrónico
        extra_checks = False

        Partner = self.env['res.partner']
        partner_ids = Partner.browse(partner_ids).exists()
        if len(partner_ids) < 2:
            return

        if len(partner_ids) > 3:
            raise UserError(_("For safety reasons, you cannot merge more than 3 contacts together. You can re-open the wizard several times if needed."))

        # Check if the list of partners to merge contains child/parent relation
        child_ids = self.env['res.partner']
        for partner_id in partner_ids:
            child_ids |= Partner.search([('id', 'child_of', [partner_id.id])]) - partner_id
        if partner_ids & child_ids:
            raise UserError(_("You cannot merge a contact with one of his parent."))

        # Check if the list of partners to merge are linked to more than one user
        if len(partner_ids.with_context(active_test=False).user_ids) > 1:
            raise UserError(_("You cannot merge contacts linked to more than one user even if only one is active."))

        # Remove dst_partner from partners to merge
        if dst_partner and dst_partner in partner_ids:
            src_partners = partner_ids - dst_partner
        else:
            ordered_partners = self._get_ordered_partner(partner_ids.ids)
            dst_partner = ordered_partners[-1]
            src_partners = ordered_partners[:-1]
        _logger.info("dst_partner: %s", dst_partner.id)

        # Make the company of all related users consistent with destination partner company
        if dst_partner.company_id:
            partner_ids.mapped('user_ids').sudo().write({
                'company_ids': [Command.link(dst_partner.company_id.id)],
                'company_id': dst_partner.company_id.id
            })

        # Call sub methods to do the merge
        self._update_foreign_keys(src_partners, dst_partner)
        self._update_reference_fields(src_partners, dst_partner)
        self._update_values(src_partners, dst_partner)

        self.env.add_to_compute(dst_partner._fields['partner_share'], dst_partner)

        self._log_merge_operation(src_partners, dst_partner)

        # Delete source partner, since they are merged
        src_partners.unlink()
