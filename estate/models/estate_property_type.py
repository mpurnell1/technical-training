from odoo import fields, models


class PropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Real Estate Property Type'
    _order = 'name'

    # Custom fields
    name = fields.Char(required=True)
    sequence = fields.Integer(default=1)

    # Relational fields
    property_ids = fields.One2many('estate.property', 'property_type_id', string="Properties")

    # Constraints
    _sql_constraints = [
        ('check_name', 'UNIQUE(name)', 'The name of the property type must be unique.')
    ]
