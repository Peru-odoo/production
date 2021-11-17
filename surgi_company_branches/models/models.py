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
     @api.model
     def get_company_id_domain(self):
          domain = "[('company_id','='," + str(self.company_id.id)+ ")]"
          return domain


     branch=fields.Many2one("surgi.company.branches",string="Branch")


class stock_location_branch_inhert(models.Model):
     _inherit = "stock.quant"
     branch=fields.Many2one(related="surgi.company.branches",string="branch",compute="_get_branch",store=True)
     
     @api.depends('location_id.branch', 'location_id.location_id.branch')
     def _get_branch(self):
          for rec in self:
               if rec.location_id.usage=="view":
                    return rec.location_id.branch
               #else:
                    #return self.location_id.location_id.branch
