from odoo import models, fields, api
class ProductProductInherit(models.Model):
    _inherit = 'product.product'

    department_ids = fields.Many2many(comodel_name="hr.department",string="Department", )

    is_sales_order = fields.Boolean(string="IS Sales",  )