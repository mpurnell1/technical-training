from odoo import fields, models

class PropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Real Estate Property Type'

    name = fields.Char(required=True)

    # Constraints
    _sql_constraints = [
        ('check_name', 'UNIQUE(name)', 'The name of the property type must be unique.')
    ]