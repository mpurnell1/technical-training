from odoo import fields, models, api
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Real Estate Property Offer'
    _order = 'price desc'

    # Custom fields
    price = fields.Float()
    status = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)

    # Computed fields
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute='_compute_date_deadline', inverse='_inverse_date_deadline')

    # Constraints
    _sql_constraints = [
        ('check_price', 'CHECK(price >= 0)', 'The offer price must be positive.'),
    ]

    # Compute methods
    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for offer in self:
            date = offer.create_date or fields.Date.today()
            offer.date_deadline = fields.Date.add(date, days=offer.validity)

    @api.depends('create_date', 'date_deadline')
    def _inverse_date_deadline(self):
        for offer in self:
            offer.validity = (offer.date_deadline - offer.create_date.date()).days

    # Object methods
    @api.model_create_multi
    def create(self, values_list):
        for values in values_list:
            property_obj = self.env['estate.property'].browse(values['property_id'])
            if property_obj.state == 'new':
                property_obj.state = 'received'
            elif property_obj.state == 'received' and property_obj.offer_ids:
                min_price = min(property_obj.offer_ids.mapped('price'))
                if float_compare(values['price'], min_price, precision_digits=2) == -1:
                    raise UserError("You cannot make an offer with a price below the lowest offer.")
        return super().create(values_list)

    # Action methods
    def action_accept(self):
        for _ in self.filtered("property_id.buyer_id"):
            raise UserError("You can only accept one offer at a time.")
        self.status = 'accepted'
        self.property_id.state = 'accepted'
        self.property_id.buyer_id = self.partner_id
        self.property_id.selling_price = self.price
        return True

    def action_refuse(self):
        for offer in self.filtered(lambda o: o.status == 'accepted'):
            offer.property_id.buyer_id = False
            offer.property_id.selling_price = 0
        self.status = 'refused'
        return True
