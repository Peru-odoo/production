from odoo import fields,models,api

class stock_location_inherit(models.Model):
    _inherit = 'stock.location'

    is_operation_location = fields.Boolean(string="Is Operation Location" )
    operation_location_freeze = fields.Boolean(string="Operation Location Freeze" , tracking=True)
    internal_transit_location = fields.Boolean(string="Internal Transit Location", tracking=True)
    delivery_order_location = fields.Boolean(string="Delivery Order Location")
    sales_order_location = fields.Boolean(string="Sales Order Location")
    warehouse_id = fields.Many2one('stock.warehouse',string="Warehouse")
    required_approval = fields.Boolean(string="Required Approval?" )
    partner_id = fields.Many2one('res.partner',string='Owner')
    exclude_from_stock_control_data = fields.Boolean(string="Exclude From Stock Control Data",
                                                     help="This field used to exclude some parent location from stock control report",)
    location_selling = fields.Boolean(string="Selling Location" , store=True)
    location_asset = fields.Boolean(string="Asset Location" , store=True)

    def freezconfirm(self):
        self.operation_location_freeze = True
        mess = {
            'title': 'Freezed',
            'message': "This Location ins Freezed"
        }
        return {'warning': mess}
        pass