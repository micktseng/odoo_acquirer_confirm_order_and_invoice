from odoo import models, fields

class PaymentAcquirer(models.Model):
    _inherit = 'payment.acquirer'

    auto_confirm = fields.Selection(selection_add=[('confirm_order_and_invoice',
                                                    'Confirm the So and invoice')],
                                    string='Order Confirmation', default='confirm_so', required=True)

