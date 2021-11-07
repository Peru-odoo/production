from odoo import fields, models, api, exceptions


class stock_quant_inherit_wizard(models.Model):
    _inherit = 'stock.quant'

    #price_unit = fields.Float(string="Unit Price")
    #u_p_usd = fields.Float(string="U. Price in USD")

    product_group = fields.Char(srting="Group", related="product_id.product_group", store=True)
    product_categ_id = fields.Many2one('product.category', related='product_id.categ_id', store=True)
    location_id_parent = fields.Many2one(related='location_id.location_id' ,string='Parent Location',store=True)
    location_selling = fields.Boolean(related='location_id.location_selling' ,string='Selling Location',store=True)
    location_id_asset = fields.Boolean(related='location_id.location_asset' ,string='Asset Location',store=True)