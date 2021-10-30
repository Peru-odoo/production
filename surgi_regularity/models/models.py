# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError, UserError


class regularity_registration_line(models.Model):
    _name = 'registration.line'

    name = fields.Char("Registration Code")
    registration_name = fields.Char("Registration Name")
    country_of_orgin = fields.Many2many(comodel_name="res.country", string="Country of Orgin")
    product_registration_number = fields.Char("registration Number")
    strlize_method = fields.Char(string="Sterilization method")
    leagal_munfacter = fields.Char("legal Manufacturer")
    acual_munfacter = fields.Many2many('acual.munfacter', string="Actual Manufacturer")
    releas_date = fields.Date(String="Release Date")
    expiry_date = fields.Date(string="Expiry date")
    attachment_product = fields.Binary(string="Attachment")
    product_forms = fields.One2many('product.regul', "registration_line")


class product_template_changes(models.Model):
    _inherit = 'product.template'

    product_type_regular = fields.Selection([
        ('instrument', 'Instrument'),
        ('impluent', 'Impluent'),

    ], string="Product Type")

    strlize_field = fields.Boolean(string="Sterile")
    item_num_ref = fields.Char("Internal Reference")
    label_ref_num = fields.Char("Label Reference")
    Product_class = fields.Selection([
        ("i", "I"), ("ii", "IIA"), ("iib", "IIB"), ("iii", "III"),
    ], string="Product Class")

    registration_line_id = fields.One2many('product.regul', "product_form_id")


class product_acual_changes(models.Model):
    _name = 'acual.munfacter'

    name = fields.Char(store=True)


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
            'view_mode': 'kanban,tree,form',
            'res_model': 'product.template',
            'type': 'ir.actions.act_window',
            'context': {'edit': 1, 'create': 0}
        }
        return value


class product_template_reg(models.Model):
    _name = 'product.regul'
    registration_line = fields.Many2one("registration.line", "registration line")
    product_form_id = fields.Many2one('product.template', string='product')
    internal_ref = fields.Char(related='product_form_id.default_code', string='internal ref')
    label_ref = fields.Char(related='product_form_id.label_ref_num', string='Label Ref')
    regis_Product_class = fields.Selection(related='product_form_id.Product_class')

    desc_regul = fields.Char("Description")
    registration_line_name = fields.Char(related="registration_line.registration_name")
    registration_line_product_registration_number = fields.Char(related="registration_line.product_registration_number")


    registration_line_leagal_munfacter = fields.Char(related="registration_line.leagal_munfacter")
    registration_line_acual_munfacter = fields.Many2many(related="registration_line.acual_munfacter")
    registration_line_releas_date = fields.Date(related="registration_line.releas_date")
    registration_line_expiry_date = fields.Date(related="registration_line.expiry_date")