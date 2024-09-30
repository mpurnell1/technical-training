from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = 'estate.property.type'
    _description = 'Real Estate Property Tag'

    name = fields.Char(required=True)
