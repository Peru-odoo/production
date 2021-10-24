from odoo import models, fields, api,exceptions ,_

from datetime import datetime,timedelta

class pick_up_and_delivery_form(models.Model):
    _name = 'pickup.delivery'

    contact_rep_id=fields.Many2one('res.partner',string='العميل',store=True,)
    contact_representative = fields.Many2one('contact.representative',string='المندوب',store=True ,domain="[('contact_id', '=', contact_rep_id)]",)
    representative_mobile = fields.Char(string="التلفون",related='contact_representative.client_representative_mobile', store=True)
    pick_up = fields.Boolean('استلام')
    delivery=fields.Boolean('تسليم')

    pickup_date=fields.Date(string='التاريخ')
    product_forms = fields.One2many('product.forms','product_contact' ,string='المنتج')
    employee_id = fields.Many2one('hr.employee' ,string='موظف الشركة')
    comments = fields.Text(string='Comments')
    product_status = fields.One2many('product.forms','product_contact')

    #################### location
    street1 = fields.Char(related='contact_rep_id.street' ,string='الشارع')
    street2 = fields.Char(related='contact_rep_id.street2'  ,string='الشارع')
    city = fields.Char(related='contact_rep_id.city' ,string='المدينة')
    country_id = fields.Char(related='contact_rep_id.country_id.name' ,string='البلد')





    @api.onchange('contact_rep_id')
    def compute_display_name(self):
        self.contact_representative = ""

class pick_up_and_repair_form(models.Model):
    _name = 'pickup.repair'

    contact_rep_id=fields.Many2one('res.partner',string='العميل',store=True,)
    contact_representative = fields.Many2one('contact.representative',string='المندوب',store=True ,domain="[('contact_id', '=', contact_rep_id)]",)
    representative_mobile = fields.Char(string="التلفون",related='contact_representative.client_representative_mobile', store=True)
    pick_up = fields.Boolean('استلام')
    repair=fields.Boolean('إصلاح')

    pickup_date=fields.Date(string='التاريخ')
    product_forms = fields.One2many('product.forms','product_repair')
    employee_id = fields.Many2one('hr.employee' ,string='موظف الشركة')
    comments = fields.Text(string='ملاحظات')
    product_repair = fields.One2many('product.forms','product_repair')
    product_status = fields.One2many('product.forms','product_repair')

    #################### location
    street1 = fields.Char(related='contact_rep_id.street' ,string='الشارع')
    street2 = fields.Char(related='contact_rep_id.street2'  ,string='الشارع')
    city = fields.Char(related='contact_rep_id.city' ,string='المدينة')
    country_id = fields.Char(related='contact_rep_id.country_id.name' ,string='البلد')







    @api.onchange('contact_rep_id')
    def compute_display_name(self):
        self.contact_representative = ""


class pick_up_Installation_form(models.Model):
    _name = 'pickup.installation'

    contact_rep_id=fields.Many2one('res.partner',string='العميل',store=True,)
    contact_representative = fields.Many2one('contact.representative',string='المندوب',store=True ,domain="[('contact_id', '=', contact_rep_id)]",)
    representative_mobile = fields.Char(string="التلفون",related='contact_representative.client_representative_mobile', store=True)
    pickup_date=fields.Date(string='تاريخ التركيب والتشغيل')
    product_forms = fields.One2many('product.forms','product_installation',store=True)
    employee_id = fields.Many2one('hr.employee' ,string='موظف الشركة',store=True)
    comments = fields.Text(string='ملاحظات')

    #################### location
    street1 = fields.Char(related='contact_rep_id.street' ,string='الشارع')
    street2 = fields.Char(related='contact_rep_id.street2'  ,string='الشارع')
    city = fields.Char(related='contact_rep_id.city' ,string='المدينة')
    country_id = fields.Char(related='contact_rep_id.country_id.name' ,string='البلد')



    order_id = fields.Many2one('sale.order',store=True,string='رقم امر التوريد')
    sale_date = fields.Datetime(related='order_id.date_order', string='تاريخ امر التوريد')



    @api.onchange('contact_rep_id')
    def compute_display_name(self):
        self.contact_representative = ""


class pick_up_Installation_form(models.Model):
    _name = 'pickup.final'

    contact_rep_id=fields.Many2one('res.partner',string='العميل',store=True,)
    contact_representative = fields.Many2one('contact.representative',string='المندوب',store=True ,domain="[('contact_id', '=', contact_rep_id)]",)
    representative_mobile = fields.Char(string="التلفون",related='contact_representative.client_representative_mobile', store=True)
    pickup_date=fields.Date(string='تاريخ التسليم')
    product_forms = fields.One2many('product.forms','product_final',store=True)
    employee_id = fields.Many2one('hr.employee' ,string='موظف الشركة',store=True)
    comments = fields.Text(string='ملاحظات')

    #################### location
    street1 = fields.Char(related='contact_rep_id.street' ,string='الشارع')
    street2 = fields.Char(related='contact_rep_id.street2'  ,string='الشارع')
    city = fields.Char(related='contact_rep_id.city' ,string='المدينة')
    country_id = fields.Char(related='contact_rep_id.country_id.name' ,string='البلد')



    order_id = fields.Many2one('sale.order',store=True,string='رقم امر التوريد')
    sale_date = fields.Datetime(related='order_id.date_order', string='تاريخ امر التوريد')



    @api.onchange('contact_rep_id')
    def compute_display_name(self):
        self.contact_representative = ""




class pick_up_Installation_form(models.Model):
    _name = 'pickup.visit'

    contact_rep_id=fields.Many2one('res.partner',string='العميل',store=True,)
    contact_representative = fields.Many2one('contact.representative',string='المندوب',store=True ,domain="[('contact_id', '=', contact_rep_id)]",)
    representative_mobile = fields.Char(string="التلفون",related='contact_representative.client_representative_mobile', store=True)
    pickup_date=fields.Date(string='تاريخ التسليم')
    product_forms = fields.One2many('product.forms','product_visit',store=True)
    employee_id = fields.Many2one('hr.employee' ,string='موظف الشركة',store=True)
    comments = fields.Text(store=True,string='ملاحظات')
    comments1 = fields.Text(store=True,string='ملاحظات')
    comments2 = fields.Text(store=True,string='ملاحظات')
    comments3= fields.Text(store=True,string='ملاحظات')
    comments4= fields.Text(store=True,string='ملاحظات')

    #################### location
    street1 = fields.Char(related='contact_rep_id.street' ,string='الشارع')
    street2 = fields.Char(related='contact_rep_id.street2'  ,string='الشارع')
    city = fields.Char(related='contact_rep_id.city' ,string='المدينة')
    country_id = fields.Char(related='contact_rep_id.country_id.name' ,string='البلد')



    inform=fields.Boolean('إبلاغ')
    planed=fields.Boolean('مخطط')
    installed=fields.Boolean('تركيب')
    insure=fields.Boolean('داخل الضمان')
    uninsure=fields.Boolean('خارج الضمان')
###############################################
    press=fields.Boolean('الضغط')
    filt=fields.Boolean('الفلاتر')
    dry=fields.Boolean('التجفيف')
    received=fields.Boolean('مسلمة')
    unreceived=fields.Boolean('غير مسلمة')
    temp=fields.Boolean('درجة الحرارة')
    timeder=fields.Boolean('مدة الدورة')
    fit_to_dry=fields.Boolean('وجود مجفف من عدمة')
    dry_or_not=fields.Boolean('ملائمة الغسيل')
    customer_vgood=fields.Boolean('ممتازة')
    customer_good=fields.Boolean('جيدة')
    customer_bad=fields.Boolean('سيئة')



    @api.onchange('contact_rep_id')
    def compute_display_name(self):
        self.contact_representative = ""





class sales_order_name(models.Model):
    _inherit = 'sale.order'


class product_forms(models.Model):
    _name = 'product.forms'
    product_form_id = fields.Many2one('product.template', string='المنتج')
    product_contact=fields.Many2one('pickup.delivery')
    product_repair = fields.Many2one('pickup.repair')
    product_installation =fields.Many2one('pickup.installation')
    product_final =fields.Many2one('pickup.final')
    product_visit =fields.Many2one('pickup.visit')

    internal_ref = fields.Char(related='product_form_id.default_code',string='رقم الكتالوج')
    specilaization = fields.Many2many('product.specializationinfos' ,string='التخصص')
    notic = fields.Char(string='ملاحظات')
    date=fields.Date(string='التاريخ')
    product_status=fields.Char('حالة الجهاز الظاهرية')
    product_sug=fields.Char('اﻷجراءت المقترحة')
    product_status_tec=fields.Char('حالة الجهاز الفنية')

class product_template_infos(models.Model):
    _inherit = 'product.template'

class forms_res_partner(models.Model):
    _inherit = 'res.partner'




class forms_specialization(models.Model):
    _inherit = 'product.specializationinfos'



class forms_res_partner_emp(models.Model):
    _inherit = 'contact.representative'
