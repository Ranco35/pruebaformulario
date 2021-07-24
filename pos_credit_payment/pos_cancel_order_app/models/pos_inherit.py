# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.misc import formatLang

class ResConfigSettings(models.TransientModel):

	_inherit = 'res.config.settings'

	order_cancel = fields.Selection([('draft', 'Cancel and Reset to Draft'),
									('delete', 'Cancel and Delete')], string="cancel_order")
	cancel_delivery_order = fields.Boolean(string="Cancel Delivery order")
	cancel_invoice = fields.Boolean(string="Cancel Invoice")

	@api.onchange('order_cancel')
	def change_order(self):
		if self.order_cancel == 'draft':
			self.cancel_invoice = False
			self.cancel_delivery_order = False

	@api.model
	def get_values(self):
		res = super(ResConfigSettings, self).get_values()
		res.update(
			order_cancel=self.env['ir.config_parameter'].sudo().get_param('pos_cancel_order_app.order_cancel'),
			cancel_delivery_order=self.env['ir.config_parameter'].sudo().get_param('pos_cancel_order_app.cancel_delivery_order'),
			cancel_invoice=self.env['ir.config_parameter'].sudo().get_param('pos_cancel_order_app.cancel_invoice'),
		)
		return res

	def set_values(self):
		super(ResConfigSettings, self).set_values()
		self.env['ir.config_parameter'].sudo().set_param('pos_cancel_order_app.order_cancel',self.order_cancel),
		self.env['ir.config_parameter'].sudo().set_param('pos_cancel_order_app.cancel_delivery_order',self.cancel_delivery_order),
		self.env['ir.config_parameter'].sudo().set_param('pos_cancel_order_app.cancel_invoice',self.cancel_invoice),

class PosOrder(models.Model):

	_inherit = "pos.order"

	def action_order_cancel(self):

		order_cancel = self.env['ir.config_parameter'].sudo().get_param('pos_cancel_order_app.order_cancel')
		cancel_delivery_order = self.env['ir.config_parameter'].sudo().get_param('pos_cancel_order_app.cancel_delivery_order')
		cancel_invoice = self.env['ir.config_parameter'].sudo().get_param('pos_cancel_order_app.cancel_invoice')

		if order_cancel == 'draft':
			self.write({'state': 'draft'})
		if order_cancel == 'delete' and cancel_delivery_order or cancel_invoice:	
			self.write({'state': 'draft'})
			if cancel_delivery_order:
				self.picking_ids.write({'state':'draft'})
				for move in self.picking_ids.move_lines:
					move.write({'state':'draft'})
					move.unlink()
				self.picking_ids.unlink()
			if cancel_invoice:
				if self.account_move:
					self.account_move.write({'state':'cancel'})
					self.account_move.posted_before = False
					for line in self.account_move.line_ids:
						(line.matched_debit_ids + line.matched_credit_ids).unlink()
					self.account_move.unlink()
			for payment in self.payment_ids:
				payment.unlink()
			self.unlink()
