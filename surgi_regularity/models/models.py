# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError, UserError


class regularity_registration_line(models.Model):
    _name = 'registration.line'



    name = fields.Char("Registration Code")
    registration_name = fields.Char("Registration Name")
    country_of_orgin = fields.Many2many(comodel_name="res.country",string="Country of Orgin")
    product_registration_number = fields.Char("registration Number")
    strlize_method = fields.Char(string="Sterilization method")
    leagal_munfacter=fields.Char("legal Manufacturer")
    acual_munfacter = fields.Many2many('acual.munfacter',"name",string="Actual Manufacturer")
    releas_date = fields.Date(String="Release Date")
    expiry_date = fields.Date(string="Expiry date")
    attachment_product = fields.Binary( string="Attachment")
#     product_forms = fields.One2many('product.template','registration_line',ondelete='cascade',)





# class product_template_changes(models.Model):
#     _inherit = 'product.template'

#     product_type_regular = fields.Selection([
#         ('instrument', 'Instrument'),
#         ('impluent', 'Impluent'),

#     ], string="Product Type")

#     strlize_field=fields.Boolean(string="Sterile")
#     item_num_ref = fields.Char("Internal Reference")
#     label_ref_num = fields.Char("Label Reference")
#     desc_regul =fields.Char("Description")
#     Product_class=fields.Selection([
#         ("i","I"),("ii","IIA"),("iib","IIB"),("iii","III"),
#     ],string="Product Class")

# #     country_of_orgin = fields.Many2many(related="registration_line.country_of_orginy",string="Country of Orgin")
#     leagal_munfacter=fields.Char(reated="registration_line.leagal_munfacter",string="legal Manufacturer")
#     acual_munfacter = fields.Many2many(reated="registration_line.acual_munfacter",string="Actual Manufacturer")
#     releas_date = fields.Date(reated="registration_line.releas_date",String="Release Date")
#     expiry_date = fields.Date(reated="registration_line.expiry_date",string="Expiry date")
#     registration_line = fields.Many2one("registration.line","registration line",ondelete='cascade')



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
            'context': {'edit':1, 'create': 0}
        }
        return value






