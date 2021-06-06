from odoo import models, fields, api
class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    partner_surgeon_id = fields.Many2one(comodel_name="res.partner", string="Surgeon")
    event_id = fields.Many2one(comodel_name="hr.expenses.event", string="Event", )


