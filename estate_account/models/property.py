from odoo import models, Command


class Property(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):
        self.env['account.move'].create({
            'partner_id': self.buyer_id.id,
            'move_type': 'out_invoice',
            'invoice_line_ids': [
                Command.create({
                    'name': f'Commission for {self.name}',
                    'quantity': 1,
                    'price_unit': self.selling_price * 0.06,
                }),
                Command.create({
                    'name': 'Administrative Fees',
                    'quantity': 1,
                    'price_unit': 100,
                })
            ]
        })
        return super(Property, self).action_sold()
