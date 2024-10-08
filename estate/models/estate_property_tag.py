from odoo import fields, models


class PropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Real Estate Property Tag'
    _order = 'name'

    # Custom fields
    name = fields.Char(required=True)
    color = fields.Integer()

    # Constraints
    _sql_constraints = [
        ('check_name', 'UNIQUE(name)', 'The name of the property tag must be unique.')
    ]
