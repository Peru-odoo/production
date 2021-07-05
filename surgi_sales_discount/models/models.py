# -*- coding: utf-8 -*-

from odoo import models, fields, api


# class surgi_sales_discount(models.Model):
#     _name = 'surgi_sales_discount.surgi_sales_discount'
#     _description = 'surgi_sales_discount.surgi_sales_discount'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
class sale_order(models.Model):
    _inherit = 'sale.order'
    discount_options = fields.Selection(
        selection=[("No Discount", "No Discount"),
                   ("Trade Discount", "Trade Discount")]
        , string="Choose Discount Type", store=True, tracking=True)
    discount_value = fields.Float('Sale Discount')
    # amount_after_discount = fields.Monetary('Amount After Discount', store=True, readonly=True,
    #                                         compute='_compute_amount_after_discount',
    #                                         )
    discount_type_id = fields.Selection(selection=[("Precent", "Precent"),("Fixed", "Fixed")], string="Choose Discount Type", store=True, tracking=True)
    def calculate_tax_fixed_total(self,quantity,unitprice,totalammount,fixedammount):
        itemprice=(quantity*unitprice)/totalammount
        itemprice_fixed=round(fixedammount/totalammount,2)*100
        return (fixedammount/totalammount)*100
    @api.onchange("discount_value")
    def change_discount_value(self):
        if self.discount_type_id=="Precent":
            self.reset_all_discount_lines(self.discount_value)
        elif self.discount_type_id=="Fixed":
            totalammountx=0
            for line in self.order_line:
                totalammountx += (line.price_unit * line.product_uom_qty)
            for line in self.order_line:
                discount=self.calculate_tax_fixed_total(line.product_uom_qty,line.price_unit,totalammountx,self.discount_value)
                line.discount = discount






    @api.onchange('discount_options')
    def change_discount_option(self):
        self.discount_value=0
        self.discount_type_id=False
        self.discount_value=0
        self.reset_all_discount_lines(0)
    @api.onchange('discount_type_id')
    def change_discount_type(self):
        self.discount_value=0
        self.reset_all_discount_lines(0)
    def reset_all_discount_lines(self,val=0):
        for line in self.order_line:
            line.discount=val

        pass
