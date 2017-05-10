import logging
from odoo import models, api
_logger = logging.getLogger(__name__)

class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    @api.model
    def form_feedback(self, data, acquirer_name):
        res = super(PaymentTransaction, self).form_feedback(data, acquirer_name)
        tx = None
        try:
            tx_find_method_name = '_%s_form_get_tx_from_data' % acquirer_name
            if hasattr(self, tx_find_method_name):
                tx = getattr(self, tx_find_method_name)(data)

            if tx.state == 'pending' and tx.acquirer_id.auto_confirm == 'confirm_order_and_invoice':
                _logger.info('<%s> transaction completed, auto-confirming order %s (ID %s)', acquirer_name,
                             tx.sale_order_id.name, tx.sale_order_id.id)
                tx.sale_order_id.with_context(send_email=True).action_confirm()

                tx.sale_order_id._force_lines_to_invoice_policy_order()
                created_invoice = tx.sale_order_id.action_invoice_create()
                created_invoice = self.env['account.invoice'].browse(created_invoice)
                if created_invoice:
                    _logger.info('<%s> transaction completed, auto-generated invoice %s (ID %s) for %s (ID %s)',
                                 acquirer_name, created_invoice.name, created_invoice.id, tx.sale_order_id.name,
                                 tx.sale_order_id.id)

                    created_invoice.action_invoice_open()
                else:
                    _logger.warning('<%s> transaction completed, could not auto-generate invoice for %s (ID %s)',
                                    acquirer_name, tx.sale_order_id.name, tx.sale_order_id.id)

                tx.write({
                    'state': 'authorized',
                    'acquirer_reference': 'confirm_order_and_invoice',
                })


        except Exception:
            _logger.exception('Fail to confirm the order or send the confirmation email%s',
                              tx and ' for the transaction %s' % tx.reference or '')

        return res