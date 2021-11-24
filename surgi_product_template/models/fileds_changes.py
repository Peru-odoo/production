from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_medical = fields.Boolean(string="Medical Product", default=False)
    is_tool = fields.Boolean(string="Is Tool", default=False)
    standard_default_code = fields.Char(string='Standard Internal Reference')
    product_group = fields.Char (srting="Group")

# class ProductProduct(models.Model):
#     _inherit = "product.product"
#
#     _sql_constraints = [
#         (
#             "default_code_uniq",
#             "unique(default_code)",
#             "Internal Reference must be unique across the database!",
#         )
#     ]

class branches_products(models.Model):
    _name = 'branches.productes'

    product_id=fields.Many2one('product.product',store=True)
    branche_name = fields.Many2one('branch.location',string="Branch", store=True)
    min_num = fields.Char(string="Minimum",store=True)
    max_num = fields.Char(string="Maximum",store=True)


class product_product_branches(models.Model):
    _inherit = 'product.product'
    branches = fields.One2many('branches.productes','product_id',store=True)