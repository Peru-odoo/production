# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import Warning

class StockWarehouseInherit(models.Model):
    _inherit = 'stock.warehouse'

    warehouse_managers_id = fields.Many2one('res.users', string="Manager")
    warehouseType= fields.Char("Warehouse Type",store=True)
    manager_lines=fields.One2many('manager.line','warehouse_id')

    stock_branches = fields.Many2one('branch.location',string='Branch',store=True)
# ================= A.Salama ==================


class branches_location_wharehouse(models.Model):
    _name= 'branch.location'
    name = fields.Char(string="Branch",store=True)

class branches_products(models.Model):
    _name = 'branches.productes'

    product_id=fields.Many2one('product.product',store=True)
    branche_name = fields.Many2one('branch.location',string="Branch", store=True)
    min_num = fields.Char(string="Minimum",store=True)
    max_num = fields.Char(string="Maximum",store=True)


class product_product_branches(models.Model):
    _inherit = 'product.product'
    branches = fields.One2many('branches.productes','product_id',store=True)