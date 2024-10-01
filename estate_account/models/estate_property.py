from odoo import models, Command


class Property(models.Model):
    _inherit = 'estate.property'

    # Action methods
    def action_sold(self):
        vals_list = []
        for record in self:
            vals_list.append({
                'partner_id': record.buyer_id.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    Command.create({
                        'name': f'Commission for {record.name}',
                        'quantity': 1,
                        'price_unit': record.selling_price * 0.06,
                    }),
                    Command.create({
                        'name': 'Administrative Fees',
                        'quantity': 1,
                        'price_unit': 100,
                    })
                ]
            })
        self.env['account.move'].create(vals_list)
        return super(Property, self).action_sold()
