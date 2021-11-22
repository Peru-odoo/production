from odoo import models, fields, api, _
import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError, UserError


class regularity_registration_line(models.Model):
    _name = 'regularity.plan'

    name = fields.Integer("Plan Number")
    plan_year = fields.Char("Plan Year")
    country_of_orgin = fields.Many2many(comodel_name="res.country", string="Country of Orgin")
    leagal_munfacter = fields.Char("legal Manufacturer")
    acual_munfacter = fields.Many2many('acual.munfacter', string="Actual Manufacturer")
    issue_date = fields.Date(String="Issue Date")
    expiry_date = fields.Date(string="Expiry date")
    attachment_page = fields.One2many('product.regul', "registration_attachment")
    registration_line = fields.Many2one('registration.line' ,string="Registration Licence")
    attachment_page = fields.One2many('product.regul', "registration_plan")
