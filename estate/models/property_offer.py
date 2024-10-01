from odoo import fields, models, api
from odoo.exceptions import UserError

class PropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Real Estate Property Offer'

    price = fields.Float()
    status = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)

    # Constraints
    _sql_constraints = [
        ('check_price', 'CHECK(price >= 0)', 'The offer price must be positive.'),
    ]

    # Computed fields
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute='_compute_date_deadline', inverse='_inverse_date_deadline')

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                date = record.create_date
            else:
                date = fields.Date.today()
            record.date_deadline = fields.Date.add(date, days=record.validity)

    @api.depends('create_date', 'date_deadline')
    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days

    # Object methods
    @api.model
    def create(self, values):
        obj = self.env['estate.property'].browse(values['property_id'])
        if obj.state == 'new':
            obj.state = 'offer_received'
        elif obj.state == 'offer_received' and \
            float_compare(values['price'], obj.best_price, precision_digits=2) > 0:
            raise UserError("You cannot make an offer with a price lower than the best offer.")
        record = super(PropertyOffer, self).create(values)
        return record

    # Action methods
    def action_accept(self):
        for record in self:
            if record.property_id.buyer_id:
                raise UserError("You can only accept one offer at a time.")
            record.status = 'accepted'
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price

    def action_refuse(self):
        for record in self:
            if record.status == 'accepted':
                record.property_id.buyer_id = False
                record.property_id.selling_price = 0
            record.status = 'refused'