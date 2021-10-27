# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError, UserError


# class surgi_regularity(models.Model):
#     _name = 'surgi_regularity.surgi_regularity'
#     _description = 'surgi_regularity.surgi_regularity'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100


class product_template_changes(models.Model):
    _inherit = 'product.template'

    product_type_regular = fields.Selection([
        ('instrument', 'Instrument'),
        ('impluent', 'Impluent'),

    ], string="Product Type")

    strlize_field=fields.Boolean(string="Sterile")
    item_num_ref = fields.Char("Internal Reference")
    label_ref_num = fields.Char("Label Reference")
    desc_regul = fields.Char(related="name",readonly=False,string="Descrption")
    Product_class=fields.Selection([
        ("i","I"),("ii","IIA"),("iib","IIB"),("iii","III"),
    ],string="Product_class")
    leagal_munfacter=fields.Char("legal Manufacturer")
    acual_munfacter = fields.Many2many('acual.munfacter',"name",string="Actual Manufacturer")
    country_of_orgin = fields.Many2one("res.country",string="Country of Orgin")


class product_template_changes(models.Model):
    _name = 'acual.munfacter'

    name = fields.Char()


class StockInherit(models.Model):
    _inherit = 'product.template'

    @api.model
    def button_stock_action(self):
        # ctx = dict(
        #     create=False,
        # )
        value = {
            'name': 'Product',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'product.template',
            'type': 'ir.actions.act_window',
            'context': {'edit':1, 'create': 0}
        }
        return value
