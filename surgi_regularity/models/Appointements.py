from odoo import models, fields, api, _
import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError, UserError


class ScientificCommitte(models.Model):
    _name = 'scientific.appointement'

    name = fields.Char(string="System Name")

    type_of_appoint = fields.Selection([('sterile', 'Sterile'),
                                        ('non_sterile', 'Non Sterile'), ], string="Type of Appointment", )
    accept_date = fields.Date(String="Acceptance Date")
    expiry_date = fields.Date(string="Expiry date")
    # product_line = fields.Many2one('product.lines', string="Product Line")

    request_id = fields.Char("Request ID", store=True)
    temp_num = fields.Char("Temporary Number", store=True)
    skus = fields.Char(string="SKUS")
    attachment_page = fields.One2many('product.regul', "registration_appointement")
    product_appintment = fields.One2many('product.regul', "registration_appointement")


class product_appint_reg(models.Model):
    _inherit = 'product.regul'

    registration_appointement = fields.Many2one("scientific.appointement", "Appointment")

    attachment_product_appointement = fields.Many2many('ir.attachment', 'class_ir_attachments_rel', 'class_id',
                                                       'attachment_id', 'Attachments')
    certifect_appointement = fields.Char("Certificate")

    product_form_appointement = fields.Many2one('product.product', string='product')
    supplier_appo = fields.Many2one(related="product_form_appointement.seller_ids.name", string="Supplier",
                                    readonly=False)
    product_line_appo = fields.Many2one(related="product_form_appointement.categ_id", string="Line")
    sterile_appo = fields.Boolean(string="Sterile", related="product_form_appointement.strlize_field")
    product_serial_appointement = fields.Many2one('stock.production.lot', string='Serial Number',
                                                  domain="[('product_id','=',product_form_appointement)]")

    @api.onchange('product_form_appointement')
    def compute_display_name(self):
        self.product_serial_appointement = ""

