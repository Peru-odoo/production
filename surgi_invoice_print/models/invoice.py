from odoo import models, fields, api
class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    is_surgi_printed = fields.Boolean(string="Is Surgi Printed")#, tracking=True
    is_printed = fields.Boolean(string="IS Printed", tracking=True)
    printed_num = fields.Integer(string="Report Number", required=False, )

    is_equal_total = fields.Boolean(string="IS Equal", store=True, compute='compute_is_equal_total2')
    is_equal_total2 = fields.Boolean(string="", compute='compute_is_equal_total2')

    @api.depends('amount_total', 'printinvoicetoline')
    def compute_is_equal_total2(self):
        for rec in self:
            rec.is_equal_total = False
            rec.is_equal_total2 = False
            total = 0.0
            for line in rec.printinvoicetoline:
                total += line.total
            if rec.amount_total == total:
                rec.is_equal_total = True
                rec.is_equal_total2 = True



class ReportAccountMovePrinted(models.AbstractModel):
    _name = 'report.surgi_invoice_print.report_invoice_demo'

    @api.model
    def _get_report_values(self, docids, data=None):

        docs = self.env['account.move'].browse(docids)

        docs.is_surgi_printed=True
        return {
            'doc_ids': docids,
            'doc_model': 'account.move',
            'docs': docs,
        }

class ReportAccountHashIntegrity(models.AbstractModel):
    _name = 'report.account.report_invoice_with_payments'
    _description = 'Get hash integrity result as PDF.'

    @api.model
    def _get_report_values(self, docids, data=None):

        docs = self.env['account.move'].browse(docids)

        docs.is_printed=True
        docs.printed_num+=1
        return {
            'doc_ids': docids,
            'doc_model': 'account.move',
            'docs': docs,
        }
