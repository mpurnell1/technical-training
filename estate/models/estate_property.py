from odoo import fields, models
from odoo.tools.date_utils import add

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'

    # Custom fields
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=add(fields.Date.today(), days=90))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([('n', 'North'), ('e', 'East'), ('s', 'South'), ('w', 'West')])

    # Reserved fields
    active = fields.Boolean(default=True)
    state = fields.Selection([
        ('new', 'New'),
        ('received', 'Offer Received'),
        ('accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled')], string="Status", default='new', copy=False)
