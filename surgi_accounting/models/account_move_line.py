from odoo import models, fields, api


class AccountAccountInherit(models.Model):
    _inherit = 'account.move.line'

    cash_group_id = fields.Many2one('account.cash.group', related='account_id.cash_group_id', string='Cash Group', readonly=False, store=True)
    account_internal_type = fields.Selection(related='account_id.user_type_id.type', string="Internal Type", readonly=True, store=True)
    account_internal_group = fields.Selection(related='account_id.user_type_id.internal_group', string="Internal Group", readonly=True, store=True)