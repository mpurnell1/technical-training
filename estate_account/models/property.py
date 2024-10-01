from odoo import fields, models
import logging

_logger = logging.getLogger(__name__)


class Property(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):
        _logger.warning('Overridden method called')
        return super(Property, self).action_sold()