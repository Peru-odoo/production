# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError, UserError


class regularity_registration_line(models.Model):
    _name = 'registration.line'

    name = fields.Char("Registration Code")
    registration_name = fields.Char("Registration Name")
    country_of_orgin = fields.Many2many(comodel_name="res.country", string="Country of Orgin")
    product_registration_number = fields.Char("registration Number")
    strlize_method = fields.Char(string="Sterilization method")
    leagal_munfacter = fields.Char("legal Manufacturer")
    acual_munfacter = fields.Many2many('acual.munfacter', string="Actual Manufacturer")
    releas_date = fields.Date(String="Release Date")
    expiry_date = fields.Date(string="Expiry date")
    product_forms = fields.One2many('product.regul', "registration_line")
    attachment_page = fields.One2many('product.regul', "registration_attachment")
    varition_num = fields.One2many('product.regul', "varition_num_registration")
    product_expiry = fields.Date("Product Expiry")
    start_date = fields.Date(string="Start date")
    end_date = fields.Date(string="End date")
    date_diff = fields.Char("Shelf Life" , compute="_get_age_from_relation")
    storge_condit = fields.Char("Storage Conditions")




    @api.depends("start_date","end_date")
    def _get_age_from_relation(self):
        """Age Calculation"""
        for stud in self:
            if stud.start_date and stud.end_date:
                """
                Get only year.
                """


                currentDate = fields.Datetime.to_datetime(stud.end_date).date()

                deadlineDate= fields.Datetime.to_datetime(stud.start_date).date()
                # print (deadlineDate)
                daysLeft = currentDate - deadlineDate
                # print(daysLeft)

                years = ((daysLeft.total_seconds())/(365.242*24*3600))
                yearsInt=int(years)

                months=(years-yearsInt)*12
                monthsInt=int(months)

                days=(months-monthsInt)*(365.242/12)
                daysInt=int(days)

                hours = (days-daysInt)*24
                hoursInt=int(hours)

                minutes = (hours-hoursInt)*60
                minutesInt=int(minutes)

                seconds = (minutes-minutesInt)*60
                secondsInt =int(seconds)

                stud.date_diff = '{0:d} years, {1:d}  months, {2:d}  days,   \
                '.format(yearsInt,monthsInt,daysInt,hoursInt)
            else:
                stud.date_diff = "Not Providated...."





class product_template_changes(models.Model):
    _inherit = 'product.template'

    product_type_regular = fields.Selection([
        ('instrument', 'Instrument'),
        ('impluent', 'Impluent'),

    ], string="Product Type")

    strlize_field = fields.Boolean(string="Sterile")
    item_num_ref = fields.Char("Internal Reference")
    label_ref_num = fields.Char("Label Reference")
    Product_class = fields.Selection([
        ("i", "I"), ("ii", "IIA"), ("iib", "IIB"), ("iii", "III"),
    ], string="Product Class")

    registration_line_id = fields.One2many('product.regul', "product_form_id")


class product_acual_changes(models.Model):
    _name = 'acual.munfacter'

    name = fields.Char(store=True)


class StockInherit(models.Model):
    _inherit = 'product.template'

    @api.model
    def button_stock_action(self):
        # ctx = dict(
        #     create=False,
        # )
        value = {
            'name': 'Product',
            'view_type': 'form',
            'view_mode': 'kanban,tree,form',
            'res_model': 'product.template',
            'type': 'ir.actions.act_window',
            'context': {'edit': 1, 'create': 0}
        }
        return value


class product_template_reg(models.Model):
    _name = 'product.regul'
    registration_line = fields.Many2one("registration.line", "registration line")
    product_form_id = fields.Many2one('product.template', string='product')
    internal_ref = fields.Char(related='product_form_id.default_code', string='internal ref')
    label_ref = fields.Char(related='product_form_id.label_ref_num', string='Label Ref')
    regis_Product_class = fields.Selection(related='product_form_id.Product_class')
    registration_plan = fields.Many2one("regularity.plan", "Plan")

    desc_regul = fields.Char("Description")
    registration_line_name = fields.Char(related="registration_line.registration_name")
    registration_line_product_registration_number = fields.Char(related="registration_line.product_registration_number")

    registration_attachment = fields.Many2one("registration.line", "registration line")

    registration_line_leagal_munfacter = fields.Char(related="registration_line.leagal_munfacter")
    registration_line_acual_munfacter = fields.Many2many(related="registration_line.acual_munfacter")
    registration_line_releas_date = fields.Date(related="registration_line.releas_date")
    registration_line_expiry_date = fields.Date(related="registration_line.expiry_date")
    attachment_product = fields.Many2many('ir.attachment', 'class_ir_attachments_rel', 'class_id', 'attachment_id', 'Attachments')
    attachment_product_plan = fields.Many2many('ir.attachment', 'class_ir_attachments_rel', 'class_id', 'attachment_id', 'Attachments')
    certifect_plan = fields.Char("Certificate")
    certifect_expiry_plan = fields.Date("Expiry")

    certifect = fields.Char("Certificate")
    certifect_expiry = fields.Date("Expiry")
    varition_num=fields.Char("Varition Number")
    varition_num_date = fields.Date("Varition Date")
    varition_num_registration = fields.Many2one("registration.line", "registration line")
