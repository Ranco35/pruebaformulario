# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class CancelOrder(models.TransientModel):

	_name = 'cancel.order'

	def cancel_order(self):
		pos_order = self.env['pos.order'].browse(self._context.get('active_ids'))
		order_cancel = self.env['ir.config_parameter'].sudo().get_param('pos_cancel_order_app.order_cancel')
		if order_cancel == 'draft':
			for order in pos_order:
				order.write({'state':'draft'})

class CancelOrder(models.TransientModel):

	_name = 'delete.order'

	def delete_order(self):
		pos_order = self.env['pos.order'].browse(self._context.get('active_ids'))
		order_cancel = self.env['ir.config_parameter'].sudo().get_param('pos_cancel_order_app.order_cancel')
		cancel_delivery_order = self.env['ir.config_parameter'].sudo().get_param('pos_cancel_order_app.cancel_delivery_order')
		cancel_invoice = self.env['ir.config_parameter'].sudo().get_param('pos_cancel_order_app.cancel_invoice')
		if order_cancel == 'delete':
			for order in pos_order:
				order.write({'state': 'draft'})
				if cancel_delivery_order:
					order.picking_ids.write({'state':'draft'})
					for move in order.picking_ids.move_lines:
						move.write({'state':'draft'})
						move.unlink()
					order.picking_ids.unlink()
				if cancel_invoice:
					order.account_move.write({'state':'cancel'})
					order.account_move.posted_before = False
					for line in order.account_move.line_ids:
						(line.matched_debit_ids + line.matched_credit_ids).unlink()
					order.account_move.unlink()
				for payment in order.payment_ids:
					payment.unlink()
		pos_order.unlink()