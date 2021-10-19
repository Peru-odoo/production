from odoo import models, fields, api
from datetime import date,datetime
class OperationOperationInherit(models.Model):
    _inherit = 'operation.operation'

    confirmed_date = fields.Date(string="Confirmed Date")
    is_operation_tracking = fields.Boolean(string="",  )
    invoice_ids = fields.Many2many(comodel_name="account.move",related='sale_order_id.invoice_ids')
    invoice_date = fields.Char(string="Invoice Date",compute='compute_invoice_date')
    collection_date = fields.Date(string="Collection Date")
    deposit_date = fields.Date(string="Deposit Date")
    payment_lines_ids = fields.Many2many(comodel_name="account.payment",string="Payment",related='sale_order_id.payment_lines_ids' )

    @api.depends('invoice_ids')
    def compute_invoice_date(self):
        for rec in self:
            all_invoice_date=''
            rec.invoice_date=False
            for inv in rec.invoice_ids:
                if inv.invoice_date:
                    all_invoice_date += str("[") +str(inv.invoice_date) + str("]")
            rec.invoice_date=all_invoice_date

    def action_confirm_sales(self):
        res=super(OperationOperationInherit, self).action_confirm_sales()

        if self.state=='confirm':
            self.confirmed_date=date.today()
        return res



    def button_operation_tracking(self):

        for rec in self:
            sale_order_record = self.env['sale.order'].search([('operation_id','=',rec.id)])
            for sale in sale_order_record:
                rec.sale_order_id=sale.id



class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    payment_lines_ids = fields.Many2many(comodel_name="account.payment", string="Payment",compute='compute_payment_lines')

    @api.depends('state','payment_reference')
    def compute_payment_lines(self):
        for rec in self:
            lines=[]
            for pay in self.env['account.payment'].search([('ref','=',rec.payment_reference)]):
                lines.append(pay.id)
            rec.payment_lines_ids=lines



class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    payment_lines_ids = fields.Many2many(comodel_name="account.payment", string="Payment",compute='compute_payment_lines')

    @api.depends('name')
    def compute_payment_lines(self):
        for rec in self:
            rec.payment_lines_ids=False
            lines=[]
            for inv in self.env['account.move'].search([('invoice_origin','=',rec.name)]):
                rec.payment_lines_ids=inv.payment_lines_ids.ids

