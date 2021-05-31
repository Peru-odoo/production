# -*- coding: utf-8 -*-

from datetime import date
from datetime import datetime
from odoo import api
from odoo import exceptions
from odoo import fields
from odoo import models
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo.tools import pytz


# class surgi_manager_reports(models.Model):
#     _name = 'surgi_manager_reports.surgi_manager_reports'
#     _description = 'surgi_manager_reports.surgi_manager_reports'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100


class operation_report_manager(models.Model):
    _inherit = 'operation.operation'

class operation_stage_reports(models.Model):
    _inherit = 'operation.stage'


class sales_order_reports(models.Model):
    _inherit = 'sale.order'

class cutomer_invoice__reports(models.Model):
    _inherit = 'account.move'


class sales_line_users_mnager(models.Model):
    _inherit = 'res.users'

    line_manger = fields.One2many("crm.team","line_manager_team")
    line_manger_category = fields.One2many("product.category","line_manager_category")

class sales_team_manager_Line(models.Model):
    _inherit = 'crm.team'

    line_manager_team = fields.Many2one("res.users", string="Line Manager")



class product_category_line_manger(models.Model):
    _inherit = 'product.category'

    line_manager_category = fields.Many2one("res.users", string="Line Manager")

class hr_expance_line_manger(models.Model):
    _inherit = 'hr.expense'





