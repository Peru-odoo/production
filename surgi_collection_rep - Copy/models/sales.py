from odoo import models, fields, api
class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    collection_rep = fields.Many2one('res.users', 'Collection Rep', track_visibility='onchange',related='partner_id.collection_rep')


class RESPartnerInherit(models.Model):
    _inherit = 'res.partner'

    collection_rep = fields.Many2one('res.users', 'Collection Rep', track_visibility='onchange')

class AccountMoveInherit(models.Model):
    _inherit = 'account.move'
    collection_rep = fields.Many2one('res.users', 'Collection Rep', track_visibility='onchange',related='partner_id.collection_rep',readonly=1)
    # field is selection(Deal - Problem - Permitted - Unpermitted)
    collection_state = fields.Selection(string="Collection Status", selection=[
        ('Deal', 'Deal'), ('Problem', 'Problem'),
        ('Permitted', 'Permitted'), ('Unpermitted', 'Unpermitted'),
    ],)



