
from odoo import models, fields, api, _

class manager_line(models.Model):
    _name = 'manager.line'
    manager_id = fields.Many2one('res.users')

    warehouse_id = fields.Many2one('stock.warehouse')


class Stock_quent_mangerInherit(models.Model):
    _inherit = 'stock.quant'

    @api.model
    def button_stock_onhand_action(self):
        # ctx = dict(
        #     create=False,
        # )
        value = {
            'name': 'Product Line Report',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'stock.quant',
            'type': 'ir.actions.act_window',
            'domain': [('on_hand', '=', True),('product_id.product_line_id.warehouse_users','=',self.env.user.id)]
        }
        return value
class sales_manger_order_mangerInherit(models.Model):
    _inherit = 'sale.order'

    @api.model
    def button_sales_manger_order_action(self):
        # ctx = dict(
        #     create=False,
        # )
        value = {
            'name': 'Product Line sales Order',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'sale.order',
            'type': 'ir.actions.act_window',
            'domain': [('team_id.product_line_id','=',self.env.user.id)]
        }
        return value
