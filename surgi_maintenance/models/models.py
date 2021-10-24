from odoo import models, fields, api,exceptions ,_





class crm_pipeline_res_partner_emp(models.Model):
    _name = 'contact.representative'
    contact_id = fields.Many2one("res.partner", string="contact",store=True)

    position_representative = fields.Char('Position',store=True)
    name = fields.Char(string="Client Name",store=True)
    client_representative_mobile = fields.Char(string="Client Mobile",store=True)

class crm_pipeline_res_partner(models.Model):
    _inherit = 'res.partner'


    erepresentative_id = fields.One2many('contact.representative','contact_id', string='Representative',store=True)


class crm_pipeline_specialization(models.Model):
    _name = 'product.specializationinfos'
    # _rec_name = 'name'
    _description = 'New Description'

    name = fields.Char(string="product specialization",store=True)
