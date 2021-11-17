# -*- coding: utf-8 -*-

from odoo import models, fields, api


class surgi_company_branches(models.Model):
     _name = 'surgi.company.branches'
     _description = 'surgi_company_branches.surgi_company_branches'

     name=fields.Char("Branch Name")
     company_id=fields.Many2one('res.company',  string="Company")


class branch_company_inhert(models.Model):
     _inherit="res.company"
     branches=fields.One2many('surgi.company.branches', 'company_id', string="Branches")


#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
class stock_location_branch_inhert(models.Model):
     _inherit = "stock.location"

     def get_company_id_domain(self):
          domain = "[('company_id','='," + self.company_id+ ")]"
          return domain


     branch=fields.Many2one("surgi.company.branches",string="Branch",domain=get_company_id_domain())


