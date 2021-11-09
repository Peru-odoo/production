from odoo import models, fields, api
from odoo.exceptions import Warning

class StockWarehouseInherit(models.Model):
    _inherit = 'stock.warehouse'
    warehouse_users = fields.Many2many('res.users', string="Users")



class stock_picking_type_changes(models.Model):
    _inherit = 'stock.picking.type'
    # add field to relate with many2many field in stock warehuse
    warehouse_users = fields.Many2many(related="warehouse_id.warehouse_users",comodel_name='res.users', string="Users")


class StockPickingInherit(models.Model):
    _inherit = 'stock.picking'

    warehouse_id_user=fields.Many2one(
        related="picking_type_id.warehouse_id")