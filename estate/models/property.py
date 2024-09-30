from odoo import fields, models, api

class Property(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'

    # Custom fields
    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(string="Available From", copy=False, default=fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([('n', 'North'), ('e', 'East'), ('s', 'South'), ('w', 'West')])

    # Computed fields
    total_area = fields.Integer(string='Total Area (sqm)', compute='_compute_total_area')
    best_price = fields.Float(string='Best Offer', compute='_compute_best_price')

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price')) or 0

    # Relational fields
    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    buyer_id = fields.Many2one('res.partner', string="Buyer", copy=False)
    salesperson_id = fields.Many2one('res.users', string="Salesperson", default=lambda self: self.env.user)
    tag_ids = fields.Many2many('estate.property.tag', string="Tags")
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")

    # Reserved fields
    active = fields.Boolean(default=True)
    state = fields.Selection(string="Status", default='new', copy=False, selection=[
        ('new', 'New'),
        ('received', 'Offer Received'),
        ('accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled')])
