from odoo import models, fields, api
class StockQuantInherit(models.Model):
    _inherit = 'stock.quant'

    usd_value = fields.Float(string="Usd Value",compute='compute_value')
    unit_cost_dollar = fields.Float(string="Usd Unit Cost",compute='compute_value')

    def compute_value(self):
        dollar_rate_rec=self.env['dollar.rate'].search([],limit=1)
        for rec in self:
            if dollar_rate_rec.value>0:
                rec.usd_value= rec.value/dollar_rate_rec.value
            else:
                rec.usd_value =0.0

            if rec.available_quantity>0:
                rec.unit_cost_dollar=rec.usd_value/rec.available_quantity
            else:
                rec.unit_cost_dollar =0.0


