from odoo import models, fields, api
class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    collection_rep = fields.Many2one('res.users', 'Collection Rep', track_visibility='onchange',)
    @api.onchange('partner_id')
    def compute_collection_rep(self):
        if self.partner_id:
            self.collection_rep=self.partner_id.collection_rep.id
        else:
            self.collection_rep =False


class RESPartnerInherit(models.Model):
    _inherit = 'res.partner'

    collection_rep = fields.Many2one('res.users', 'Collection Rep', track_visibility='onchange')

class AccountMoveInherit(models.Model):
    _inherit = 'account.move'
    collection_rep = fields.Many2one('res.users', 'Collection Rep', track_visibility='onchange'
                                     )
    # , related = 'partner_id.collection_rep',
    # field is selection(Deal - Problem - Permitted - Unpermitted)
    collection_state = fields.Selection(string="Collection Status", selection=[
        ('Deal', 'Deal'), ('Problem', 'Problem'),
        ('Permitted', 'Permitted'), ('Unpermitted', 'Unpermitted'),
    ],)
    is_collection_rep = fields.Boolean(string="",compute='compute_is_collection_rep'  )
    @api.depends('partner_id')
    def compute_is_collection_rep(self):
        for rec in self:
            rec.is_collection_rep=False
            if self.partner_id:
                rec.collection_rep = rec.partner_id.collection_rep.id
                rec.is_collection_rep = True
            else:
                self.collection_rep = False





