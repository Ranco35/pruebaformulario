
odoo.define('pos_credit_payment.pos', function (require) {
	"use strict";

	var models = require('point_of_sale.models');
	var core = require('web.core');
	var rpc = require('web.rpc');
	

	var _t = core._t;
	var _super_posmodel = models.PosModel.prototype;
	models.PosModel = models.PosModel.extend({
		initialize: function (session, attributes) {
			var partner_model = _.find(this.models, function(model){ return model.model === 'res.partner'; });
			partner_model.fields.push('custom_credit');
			
			var journal_model = _.find(this.models, function(model){ return model.model === 'pos.payment.method'; });
			journal_model.fields.push('credit_jr','cash_journal_id');
			return _super_posmodel.initialize.call(this, session, attributes);
		},
	});

	let OrderSuper = models.Order.prototype;
	models.Order = models.Order.extend({
		initialize: function(attributes, options) {
			OrderSuper.initialize.apply(this, arguments);
			let self = this;
			setInterval(function(){ 
				self.pos.load_new_partners();
			}, 5000);
		},
	});
});
