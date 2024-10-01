from odoo import fields, models


class Users(models.Model):
    _inherit = 'res.users'

    # Custom fields
    property_ids = fields.One2many('estate.property', 'salesperson_id', string="Properties", domain=[('state', 'not in', ('accepted', 'sold'))])
