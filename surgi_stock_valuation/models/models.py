# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class surgi_stock_valuation(models.Model):
#     _name = 'surgi_stock_valuation.surgi_stock_valuation'
#     _description = 'surgi_stock_valuation.surgi_stock_valuation'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
