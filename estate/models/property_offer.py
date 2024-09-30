from odoo import fields, models, api

class PropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Real Estate Property Offer'

    price = fields.Float()
    status = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)

    # Computed fields
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute='_compute_date_deadline', inverse='_inverse_date_deadline')

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add(record.create_date, days=record.validity)

    @api.depends('create_date', 'date_deadline')
    def _inverse_date_deadline(self):
        for record in self:
            record.validity = fields.Date.subtract(record.date_deadline, record.create_date).days
