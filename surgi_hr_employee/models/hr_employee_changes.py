from odoo import api, _
from odoo import fields
from odoo import models
from odoo.models import _logger
from odoo.exceptions import ValidationError
import datetime
from dateutil import relativedelta
from datetime import date,datetime


class stage_scholarship(models.Model):
    _name = 'scholarship.stage'
    # _rec_name = 'name'

    name = fields.Char(string="المرحلة الدراسية")

class Employee_relations(models.Model):
    _name ='emp.relations'

    employee_realtion_id = fields.Many2one('hr.employee',string='Employee Relations')
    emp_family_name = fields.Char(string="Name")
    attachment_family = fields.Binary( string="Attachment")

    employee_relation = fields.Selection([('wifes', 'Wife'), ('husbands', 'Husband'), ('sons', 'Son'), ('daughters', 'Daughter')])
    emp_family_gender = fields.Char(compute='_auto_gender_generate', string="Gender",store=True)

    bdate = fields.Date(string="Date Of Birth")
    relation_age = fields.Char(string="Age", compute="_get_age_from_relation", store=True)





    @api.depends("employee_relation")
    def _auto_gender_generate(self):
        for rec in self:
            if rec.employee_relation == "wifes":
                rec.emp_family_gender = 'Female'
            elif rec.employee_relation == "husbands":
                rec.emp_family_gender = 'Male'
            elif rec.employee_relation == "sons":
                rec.emp_family_gender = 'Male'
            elif rec.employee_relation == "daughters":
                rec.emp_family_gender = 'Female'
            else:
                rec.emp_family_gender = "Not Providated...."


    @api.depends("bdate")
    def _get_age_from_relation(self):
        """Age Calculation"""
        today_date = datetime.date.today()
        for stud in self:
            if stud.bdate:
                """
                Get only year.
                """
                # bdate = fields.Datetime.to_datetime(stud.bdate).date()
                # total_age = str(int((today_date - bdate).days / 365))
                # stud.relation_age = total_age


                currentDate = datetime.date.today()

                deadlineDate= fields.Datetime.to_datetime(stud.bdate).date()
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

                stud.relation_age = '{0:d} years, {1:d}  months, {2:d}  days,   \
                old.'.format(yearsInt,monthsInt,daysInt,hoursInt)
            else:
                stud.relation_age = "Not Providated...."


class Employee_scholarship(models.Model):
    _name ='emp.scholarship'

    name = fields.Many2one('hr.employee',string='اسم الموظف')
    # employee_scholarship_code = fields.Many2one('hr.employee', related='employee_id.registration_number' ,string='Employee Code')
    employee_scholarship_code = fields.Char(string="كود الموظف",
                                      related='name.registration_number',store=True)
    employee_scholarship_wl = fields.Char(string="منطقة العمل",
                                      related='name.work_location', store=True)
    emp_scholarship_name = fields.Char(string="أسم الابن")
    # attachment_ids = fields.Binary( string="Attachment")
    attachment_brith = fields.Binary( string="شهادة الميلاد")
    attachment_grade = fields.Binary( string="شهادة اخر مرحلة")
    attachment_other = fields.Binary( string="اخري")

    employee_relation = fields.Selection([ ('sons', 'ابن'), ('daughters', 'أبنة')])
    emp_family_gender = fields.Char(compute='_auto_gender_generate', string="النوع",store=True)

    bdate = fields.Date(string="تاريخ الميلاد")
    relation_age = fields.Char(string="السن", compute="_get_age_from_relation", store=True)
    school_type = fields.Selection([ ('ar', 'عربي'),('gr', 'ألماني'), ('fr', 'فرنساوي'), ('en', 'انجليزي'),('co', 'تجاري'),('de', 'تجريبي'),('cr', 'صنايع') ])
    school_stage = fields.Many2one('scholarship.stage' ,string="المرحلة الدراسية")
    school_year = fields.Selection([ ('one', '1'), ('two', '2'),('three', '3'), ('four', '4'),('five', '5'), ('six', '6')])
    school_percentage = fields.Char(string="نسبة النجاح لأخر مرحلة دارسية")




    @api.depends("employee_relation")
    def _auto_gender_generate(self):
        for rec in self:

            if rec.employee_relation == "sons":
                rec.emp_family_gender = 'ذكر'
            elif rec.employee_relation == "daughters":
                rec.emp_family_gender = 'انثي'
            else:
                rec.emp_family_gender = "Not Providated...."


    @api.depends("bdate")
    def _get_age_from_relation(self):
        """Age Calculation"""
        today_date = datetime.date.today()
        for stud in self:
            if stud.bdate:
                """
                Get only year.
                """
                # bdate = fields.Datetime.to_datetime(stud.bdate).date()
                # total_age = str(int((today_date - bdate).days / 365))
                # stud.relation_age = total_age


                currentDate = datetime.date.today()

                deadlineDate= fields.Datetime.to_datetime(stud.bdate).date()
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

                stud.relation_age = '{0:d} years, {1:d}  months,   \
                old.'.format(yearsInt,monthsInt,daysInt,hoursInt)
            else:
                stud.relation_age = "Not Providated...."


class DepartmentFields(models.Model):
    _inherit = 'hr.department'

    department_type = fields.Selection([('department', 'Main Department'), ('section', 'Section')], string='Type',
                                       translate=True)

class HrEmployeeBaseDate(models.AbstractModel):
    _inherit = "hr.employee.base"

    resignation_date = fields.Date()
    labor_linc_no = fields.Char(string="Labor Linc No.", )
    id_from = fields.Char(string="ID From", store=True)
    military_status = fields.Selection(string="Military Status",
                                       selection=[('not applicable', 'Not Applicable'), ('postponed', 'Postponed'),
                                                  ('exempted', 'Exempted'), ('completed', 'Completed'),
                                                  ('current', 'Currently serving ')], store=True)
    military_number = fields.Char(string="Military Number", store=True)


    religion = fields.Selection(string="Religion",
                                selection=[('muslim', 'Muslim'), ('christian', 'Christian'), ('other', 'Others')])
    social_ins_exist = fields.Boolean("Has Social Insurance")
    social_ins_no = fields.Integer(string="Soical Ins No.")
    social_ins_title = fields.Char(string="Social Job Title")
    medical_ins_exist = fields.Boolean("Has Medical Insurance")
    medical_company = fields.Selection(string="Medical Co.", selection=[('inaya', 'Inaya')])
    medical_number = fields.Integer(string="Medical No.")
    mi_date = fields.Date(string="Medical Insurance Date", help='Medical  Insurance Date')
    section_id = fields.Many2one('hr.department', string="Section", domain=[('department_type', '=', 'section')])
    full_employee_name = fields.Char(string="Full Name", translate=True)
    attendance_type = fields.Selection([('in_door', 'IN Door'), ('out_door', 'Out Door')], string='Attendance type')
    in_direct_parent_id = fields.Many2one('hr.employee', 'Indirect Manager')
    age = fields.Integer(string="Age", compute="_calculate_age", store=True)  # compute="_calculate_age",
    start_date = fields.Date(string="Start Working At")
    edu_phase = fields.Many2one(comodel_name="hr.eg.education", string="Education")
    edu_school = fields.Many2one(comodel_name="hr.eg.school", string="School/University/Institute")
    edu_major = fields.Char(string="major")
    edu_grad = fields.Selection([('ex', 'Excellent'), ('vgod', 'Very Good'), ('god', 'Good'), ('pas', 'Pass')],
                                string="Grad")
    grad_year = fields.Date(string="Grad. Year")
    edu_note = fields.Text("Education Notes")
    experience_y = fields.Integer(compute="_calculate_experience", string="Experience",
                                  help="experience in our company", store=True)
    experience_m = fields.Integer(compute="_calculate_experience", string="Experience monthes", store=True)
    experience_d = fields.Integer(compute="_calculate_experience", string="Experience dayes", store=True)
    payrolled_employee = fields.Boolean("Payrolled Employee", track_visibility='onchange')
    employee_arabic_name = fields.Char(string="Arabic Name")
    private_num = fields.Char(string="Private Number ", required=False, )





    # @api.onchange('dob')
    # def get_age(self):
    #     res = {}
    #     if self.dob:
    #         dob = datetime.strptime(self.dob, "%Y-%m-%d")
    #     age_calc = (datetime.today() - dob).days / 365
    #     emp_age_family = str(age_calc) + ' Years'
    #     self.emp_age_family = emp_age_family

# class HREmployeeFields(models.Model):
#     _inherit = 'hr.employee.public'
#
#     labor_linc_no = fields.Char(string="Labor Linc No.", )
#     id_from = fields.Char(string="ID From", store=True)
#     military_status = fields.Selection(string="Military Status",
#                                        selection=[('not applicable', 'Not Applicable'), ('postponed', 'Postponed'),
#                                                   ('exempted', 'Exempted'), ('completed', 'Completed'),
#                                                   ('current', 'Currently serving ')], store=True)
#     military_number = fields.Char(string="Military Number", store=True)
#
#     # @api.model
#     # def _get_fields(self):
#     #     return ','.join('emp.%s' % name for name, field in self._fields.items() if
#     #                     if field.store and field.type not in ['many2many', 'one2many'])
#
#
#     religion = fields.Selection(string="Religion",
#                                 selection=[('muslim', 'Muslim'), ('christian', 'Christian'), ('other', 'Others')])
#     social_ins_exist = fields.Boolean("Has Social Insurance")
#     social_ins_no = fields.Integer(string="Soical Ins No.")
#     social_ins_title = fields.Char(string="Social Job Title")
#     medical_ins_exist = fields.Boolean("Has Medical Insurance")
#     medical_company = fields.Selection(string="Medical Co.", selection=[('inaya', 'Inaya')])
#     medical_number = fields.Integer(string="Medical No.")
#     mi_date = fields.Date(string="Medical Insurance Date", help='Medical  Insurance Date')
#     section_id = fields.Many2one('hr.department', string="Section", domain=[('department_type', '=', 'section')])
#     full_employee_name = fields.Char(string="Full Name", translate=True)
#     attendance_type = fields.Selection([('in_door', 'IN Door'), ('out_door', 'Out Door')], string='Attendance type')
#     in_direct_parent_id = fields.Many2one('hr.employee', 'Indirect Manager')
#     age = fields.Integer(string="Age", compute="_calculate_age", store=True)  # compute="_calculate_age",
#     start_date = fields.Date(string="Start Working At")
#     edu_phase = fields.Many2one(comodel_name="hr.eg.education", string="Education")
#     edu_school = fields.Many2one(comodel_name="hr.eg.school", string="School/University/Institute")
#     edu_major = fields.Char(string="major")
#     edu_grad = fields.Selection([('ex', 'Excellent'), ('vgod', 'Very Good'), ('god', 'Good'), ('pas', 'Pass')],
#                                 string="Grad")
#     grad_year = fields.Date(string="Grad. Year")
#     edu_note = fields.Text("Education Notes")
#     experience_y = fields.Integer(compute="_calculate_experience", string="Experience",
#                                   help="experience in our company", store=True)
#     experience_m = fields.Integer(compute="_calculate_experience", string="Experience monthes", store=True)
#     experience_d = fields.Integer(compute="_calculate_experience", string="Experience dayes", store=True)
#     payrolled_employee = fields.Boolean("Payrolled Employee", track_visibility='onchange')
#     employee_arabic_name = fields.Char(string="Arabic Name")
#     private_num = fields.Char(string="Private Number ", required=False, )


class HREmployeeFields(models.Model):
    _inherit = 'hr.employee'

    employee_family_id = fields.One2many('emp.relations','employee_realtion_id', string='Employee Relation')
    employee_scholarship_id = fields.One2many('emp.scholarship','name', string='Employee Scholarship')


    # labor_linc_no = fields.Char(string="Labor Linc No.", )
    # id_from = fields.Char(string="ID From", store=True)
    # military_status = fields.Selection(string="Military Status",
    #                                    selection=[('not applicable', 'Not Applicable'), ('postponed', 'Postponed'),
    #                                               ('exempted', 'Exempted'), ('completed', 'Completed'),
    #                                               ('current', 'Currently serving ')], store=True)
    # military_number = fields.Char(string="Military Number", store=True)
    # religion = fields.Selection(string="Religion",
    #                             selection=[('muslim', 'Muslim'), ('christian', 'Christian'), ('other', 'Others')])
    # social_ins_exist = fields.Boolean("Has Social Insurance")
    # social_ins_no = fields.Integer(string="Soical Ins No.")
    # social_ins_title = fields.Char(string="Social Job Title")
    # medical_ins_exist = fields.Boolean("Has Medical Insurance")
    # medical_company = fields.Selection(string="Medical Co.", selection=[('inaya', 'Inaya')])
    # medical_number = fields.Integer(string="Medical No.")
    # mi_date = fields.Date(string="Medical Insurance Date", help='Medical  Insurance Date')
    # section_id = fields.Many2one('hr.department', string="Section", domain=[('department_type', '=', 'section')])
    # full_employee_name = fields.Char(string="Full Name", translate=True)
    # attendance_type = fields.Selection([('in_door', 'IN Door'), ('out_door', 'Out Door')], string='Attendance type')
    # in_direct_parent_id = fields.Many2one('hr.employee', 'Indirect Manager')
    # age = fields.Integer(string="Age", compute="_calculate_age", store=True)  # compute="_calculate_age",
    # start_date = fields.Date(string="Start Working At")
    # edu_phase = fields.Many2one(comodel_name="hr.eg.education", string="Education")
    # edu_school = fields.Many2one(comodel_name="hr.eg.school", string="School/University/Institute")
    # edu_major = fields.Char(string="major")
    # edu_grad = fields.Selection([('ex', 'Excellent'), ('vgod', 'Very Good'), ('god', 'Good'), ('pas', 'Pass')],
    #                             string="Grad")
    # grad_year = fields.Date(string="Grad. Year")
    # edu_note = fields.Text("Education Notes")
    # experience_y = fields.Integer(compute="_calculate_experience", string="Experience",
    #                               help="experience in our company", store=True)
    # experience_m = fields.Integer(compute="_calculateregistration_number_experience", string="Experience monthes", store=True)
    # experience_d = fields.Integer(compute="_calculate_experience", string="Experience dayes", store=True)
    # payrolled_employee = fields.Boolean("Payrolled Employee", track_visibility='onchange')
    # employee_arabic_name = fields.Char(string="Arabic Name")
    # private_num = fields.Char(string="Private Number ", required=False, )



    # bank_account_num = fields.Integer(string="Bank Account Number",)

    def _is_name(self, name):
        return not any(char.isdigit() for char in name)

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        """ _name_search(name='', args=None, operator='ilike', limit=100, name_get_uid=None) -> ids

               Private implementation of name_search, allows passing a dedicated user
               for the name_get part to solve some access rights issues.
               """
        args = list(args or [])
        # optimize out the default criterion of ``ilike ''`` that matches everything
        if not self._rec_name:
            _logger.warning("Cannot execute name_search, no _rec_name defined on %s", self._name)
        elif not (name == '' and operator == 'ilike'):
            if self._name == 'hr.employee' and not self._is_name(name):
                args += [('registration_number', operator, name)]
            else:
                args += [(self._rec_name, operator, name)]
        return self._search(args, limit=limit, access_rights_uid=name_get_uid)

    @api.constrains('in_direct_parent_id')
    def _check_parent_id(self):
        for employee in self:
            if not employee._check_recursion():
                raise ValidationError(_('Error! You cannot create recursive hierarchy of Employee(s).'))

    @api.onchange('section_id')
    def _onchange_department(self):
        self.parent_id = self.section_id.manager_id

    @api.depends("birthday")
    def _calculate_age(self):
        for emp in self:
            if emp.birthday:
                dob = datetime.strptime(str(emp.birthday), "%Y-%m-%d").date()
                emp.age = int(int((date.today() - dob).days) / 365)
            else:
                emp.age = 0

    #
    @api.depends("start_date")
    def _calculate_experience(self):
        for emp in self:
            if emp.start_date:
                date_format = '%Y-%m-%d'
                current_date = (date.today()).strftime(date_format)
                d1 = datetime.strptime(str(emp.start_date), date_format).date()
                d2 = datetime.strptime(current_date, date_format).date()
                # r = relativedelta(d2, d1)
                r = relativedelta.relativedelta(d2, d1)

                emp.experience_y = r.years
                emp.experience_m = r.months
                emp.experience_d = r.days

    def _cron_employee_age(self):
        employee_obj = self.env['hr.employee'].search([])
        for rec in employee_obj:
            if rec.birthday:
                dob = datetime.strptime(str(rec.birthday), "%Y-%m-%d").date()
                rec.age = int(int((date.today() - dob).days) / 365)
                print('+++++++++++++++++++', rec.age)
            else:
                rec.age = 0

    def _cron_employee_exp(self):
        for emp in self.search([]):
            if emp.start_date:
                date_format = '%Y-%m-%d'
                current_date = (date.today()).strftime(date_format)
                d1 = datetime.strptime(str(emp.start_date), date_format).date()
                d2 = datetime.strptime(current_date, date_format).date()
                r = relativedelta.relativedelta(d2, d1)

                emp.experience_y = r.years
                emp.experience_m = r.months
                emp.experience_d = r.days


class dhn_hr__eg_education(models.Model):
    _name = "hr.eg.education"

    name = fields.Char(string="Education", translate=True)
    note = fields.Char(string="Note", required=False, )


class hr_eg_school(models.Model):
    _name = "hr.eg.school"

    name = fields.Char(string="School name", translate=True)
    note = fields.Char(string="Note", required=False, )
