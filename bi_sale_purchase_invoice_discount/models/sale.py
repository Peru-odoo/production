# -*- coding: utf-8 -*-
################################################################################
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
################################################################################

from odoo.osv import osv
import odoo.addons.decimal_precision as dp
from odoo.tools.translate import _
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import datetime

class sale_order(models.Model):
    _inherit = 'sale.order'

    analytic_account_id = fields.Many2one('account.analytic.account','Analytic Account')
    discount_anlytic_line_id = fields.Many2one('account.analytic.line','Discount Line')


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"
    _description = "Sales Advance Payment Invoice"  

             
class sale_order(models.Model):
    _inherit = 'sale.order'
    
    @api.model
    def create(self, vals):
        res = super(sale_order, self).create(vals)
        discount_type_percent = self.env['ir.model.data'].xmlid_to_res_id('bi_sale_purchase_invoice_discount.discount_type_percent_id')
        discount_type_fixed = self.env['ir.model.data'].xmlid_to_res_id('bi_sale_purchase_invoice_discount.discount_type_fixed_id')
        discount_type_obj = self.env['discount.type']
        if vals.get('discount_type_id') == discount_type_percent :
            brw_type = discount_type_obj.browse(discount_type_percent).discount_value
            if brw_type > 0.0:
                if vals.get('discount_value',0.00) > brw_type:
                    raise UserError(
                _('You can not set Discount Value more then %s . \n Maximum Discount value is %s \n Set maximum value Purchase-> Configuration-> Discount Type') % \
                    (brw_type , brw_type))
        if vals.get('discount_type_id') == discount_type_fixed :
            brw_type = discount_type_obj.browse(discount_type_fixed).discount_value
            if brw_type > 0.0:
                if vals.get('discount_value',0.00) > brw_type:
                    raise UserError(
                _('You can not set Discount Value more then %s. \n Maximum Discount value is %s \n Set maximum value Purchase-> Configuration-> Discount Type' ) % \
                    (brw_type ,brw_type ))
        return res
    
    
    def write(self, vals):
        discount_type_percent = self.env['ir.model.data'].xmlid_to_res_id('bi_sale_purchase_invoice_discount.discount_type_percent_id')
        discount_type_fixed = self.env['ir.model.data'].xmlid_to_res_id('bi_sale_purchase_invoice_discount.discount_type_fixed_id')
        discount_type_obj = self.env['discount.type']
        if vals.get('discount_type_id') == discount_type_percent:
            brw_type = discount_type_obj.browse(discount_type_percent).discount_value
            if brw_type > 0.0:
                if vals.get('discount_value',0.00) > brw_type:
                    raise UserError(
                _('You can not set Discount Value more then %s. \n Maximum Discount value is %s \n Set maximum value Purchase-> Configuration-> Discount Type') % \
                    (brw_type , brw_type))
        if vals.get('discount_value'):
            if self.discount_type_id.id == discount_type_percent:
                brw_type = discount_type_obj.browse(discount_type_percent).discount_value
                if brw_type > 0.0:
                    if vals.get('discount_value') > brw_type:
                        raise UserError(
                    _('You can not set Discount Value more then %s. \n Maximum Discount value is %s \n Set maximum value Purchase-> Configuration-> Discount Type') % \
                        (brw_type , brw_type))
            
            elif self.discount_type_id.id == discount_type_fixed:
                brw_type = discount_type_obj.browse(discount_type_fixed).discount_value
                if brw_type > 0.0:
                    if vals.get('discount_value',0.00) > brw_type:
                        raise UserError(
                    _('You can not set Discount Value more then %s. \n Maximum Discount value is %s \n Set maximum value Purchase-> Configuration-> Discount Type' ) % \
                        (brw_type ,brw_type ))
        if vals.get('discount_type_id') == discount_type_fixed:
            brw_type = discount_type_obj.browse(discount_type_fixed).discount_value
            if brw_type > 0.0:
                if vals.get('discount_value',0.00) > brw_type:
                    raise UserError(
                _('You can not set Discount Value more then %s. \n Maximum Discount value is %s \n Set maximum value Purchase-> Configuration-> Discount Type' ) % \
                    (brw_type ,brw_type ))
        res = super(sale_order, self).write(vals)
        return res
    
    @api.onchange('apply_discount')
    def onchange_apply_discount(self):
        if self.apply_discount:
            account_search = self.env['account.account'].search([('discount_account', '=', True),('user_type_id.internal_group','=','expense')])
            if account_search:
                self.discount_account = account_search[0].id
    
    @api.depends('order_line.price_total', 'discount_value', 'discount_type_id', 'apply_discount')
    def _amount_all(self):
        for order in self:            
            amount_untaxed = amount_tax = 0.0
            for line in order.order_line:
                amount_untaxed += line.price_subtotal
                amount_tax += line.price_tax
            if order.apply_discount == True:
                order.update({
                    'amount_untaxed': amount_untaxed,
                    'amount_tax': amount_tax,
                    'amount_total': order.amount_after_discount + amount_tax,
                })
            else:
                order.update({
                    'amount_untaxed': amount_untaxed,
                    'amount_tax': amount_tax,
                    'amount_total': amount_untaxed + amount_tax,
                })

    
    @api.depends('discount_value', 'order_line.price_total','discount_type_id')
    def _compute_amount_after_discount(self):
        discount = 0.0
        amount_untaxed = 0.0
        discount_type_percent = self.env['ir.model.data'].xmlid_to_res_id('bi_sale_purchase_invoice_discount.discount_type_percent_id')
        
        discount_type_fixed = self.env['ir.model.data'].xmlid_to_res_id('bi_sale_purchase_invoice_discount.discount_type_fixed_id')
        for self_obj in self:
            for line in self_obj.order_line:
                amount_untaxed += line.price_subtotal
            if self_obj.discount_type_id.id == discount_type_fixed:
                discount = amount_untaxed - self_obj.discount_value
                self_obj.amount_after_discount = discount
            elif self_obj.discount_type_id.id == discount_type_percent:
                discount_percent = amount_untaxed * ((self_obj.discount_value or 0.0) / 100.0)
                discount = amount_untaxed - discount_percent
                self_obj.amount_after_discount = discount
            else:
                self_obj.amount_after_discount = discount
     
    
    def _prepare_invoice(self):
        invoice_vals = super(sale_order, self)._prepare_invoice()
        invoice_vals.update({
                'discount_type_id' : self.discount_type_id.id,
                'discount_value' : self.discount_value,
                'amount_after_discount' : self.amount_after_discount,
                'out_discount_account' : self.discount_account.id,
                'apply_discount' : self.apply_discount,
            })
        return invoice_vals
        
    apply_discount = fields.Boolean('Apply Discount')
    discount_type_id = fields.Many2one('discount.type', 'Discount Type')
    discount_value = fields.Float('Sale Discount')
    discount_account = fields.Many2one('account.account', 'Discount Account')
    amount_after_discount = fields.Monetary('Amount After Discount' , store=True, readonly=True , compute = '_compute_amount_after_discount',digits_compute=dp.get_precision('Account'))

