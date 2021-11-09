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


class stock_quant_inherit_wizard(models.Model):
    _inherit = 'stock.quant'


    is_wh_user = fields.Boolean(default=False, compute=_get_wh_user,store=True)

    @api.depends('location_id.warehouse_id.warehouse_users')
    def _get_wh_user(self):
        for obj in self:
            for user in obj.location_id.warehouse_id.warehouse_users:
                if(self.env.user.id == user.id):
                    obj.is_wh_user=True
                    break
                print ("WH result: ",obj.is_wh_user)
