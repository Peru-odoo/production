from odoo import models, fields, api, _
import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError, UserError




class ScientificCommitte(models.Model):
    _name = 'scientific.committee'

    name = fields.Many2one("product.template",string="Product")
    scientific_committe_num = fields.Char("SN")

    description = fields.Text("Description",help="Scientific Committee Description")
    issue_date = fields.Date(String="Issue Date",help="Scientific Committee Issue Date")
    expiry_date = fields.Date(string="Expiry date",help="Scientific Committee Expiry Date")
    registration_line = fields.Many2one('registration.line' ,string="Registration Licence")
    registration_plan = fields.Many2one('regularity.plan' ,string="Regularity Plan")

    sterile=fields.Boolean(string="Sterile",related="name.strlize_field")
    product_class = fields.Selection(string="Class", related="name.Product_class")
    supplier = fields.One2many(related="name.saller_ids.name",string="Supplier")
