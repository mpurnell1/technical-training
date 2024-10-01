from odoo import fields, models
import logging

_logger = logging.getLogger(__name__)


class Property(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):
        self.env['account.move'].create({'partner_id': self.buyer_id.id, 'move_type': 'out_invoice'})
        return super(Property, self).action_sold()