from odoo import fields, models, api
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
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

    # Relational fields
    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    buyer_id = fields.Many2one('res.partner', string="Buyer", copy=False)
    salesperson_id = fields.Many2one('res.users', string="Salesperson", default=lambda self: self.env.user)
    tag_ids = fields.Many2many('estate.property.tag', string="Tags")
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")

    # Constraints
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price >= 0)', 'The expected price must be strictly positive.'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'The selling price must be positive.'),
    ]

    # Reserved fields
    active = fields.Boolean(default=True)
    state = fields.Selection(string="Status", default='new', copy=False, selection=[
        ('new', 'New'),
        ('received', 'Offer Received'),
        ('accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled')])

    # Compute methods
    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for property in self:
            property.best_price = max(property.offer_ids.mapped('price') or [0])

    @api.onchange('garden')
    def _onchange_garden(self):
        if not self.garden:
            self.garden_area = 0
            self.garden_orientation = False
        else:
            self.garden_area = 10
            self.garden_orientation = 'n'

    # Constraint methods
    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for property in self:
            if not float_is_zero(property.selling_price, precision_digits=2) and \
                float_compare(property.selling_price, (property.expected_price*9/10), precision_digits=2) == -1:
                raise UserError("The selling price must be at least 90% of the expected price.")

    # Object methods
    @api.ondelete(at_uninstall=False)
    def _unlink_if_new_or_cancelled(self):
        for _ in self.filtered(lambda p: p.state not in ['new', 'canceled']):
            raise UserError("You cannot delete a property that is not new or canceled.")

    # Action methods
    def action_sold(self):
        for _ in self.filtered(lambda p: p.state == 'canceled'):
            raise UserError("You cannot sell a canceled property.")
        self.state = 'sold'
        return True

    def action_cancel(self):
        for _ in self.filtered(lambda p: p.state == 'sold'):
            raise UserError("You cannot cancel a sold property.")
        self.state = 'canceled'
        return True
