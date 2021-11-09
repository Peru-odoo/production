# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import Warning

class StockWarehouseInherit(models.Model):
    _inherit = 'stock.warehouse'

    warehouse_managers_id = fields.Many2one('res.users', string="Manager")
    
    manager_lines=fields.One2many('manager.line','warehouse_id')

    stock_branches = fields.Many2one('branch.location',string='Branch',store=True)
# ================= A.Salama ==================


class branches_location_wharehouse(models.Model):
    _name= 'branch.location'
    name = fields.Char(string="Branch",store=True)
