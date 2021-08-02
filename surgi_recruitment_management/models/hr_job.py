from odoo import models, fields, api, _
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from werkzeug.urls import url_join
from datetime import datetime


class Grade(models.Model):
    _inherit = 'grade.grade'

    replacement_period = fields.Integer('Replacement Period')


class HRJob(models.Model):
    _inherit = 'hr.job'

    job_state = fields.Selection([
        ('draft', 'Draft'),
        ('hr', 'HR Approved'),
        ('gm', 'GM Approved')
    ], string='Status', readonly=True, required=True, tracking=True, copy=False, default='draft',
        help="Set whether the recruitment process for this job position.")
    grade_id = fields.Many2one(
        'grade.grade', string='Grade')
    replacement_period = fields.Integer(related='grade_id.replacement_period')
    state = fields.Selection([
        ('recruit', 'Recruitment in Progress'),
        ('open', 'Not Recruiting')
    ], string='Post Status', readonly=True, required=True, tracking=True, copy=False, default='open',
        help="Set whether the recruitment process is open or closed for this job position.")

    current_pipeline = fields.Integer('Current Pipeline', compute='_compute_current_pipeline')
    max_cv = fields.Integer('Max CVs')
    deduction = fields.Integer('Deduction')
    deduction_type = fields.Selection([
        ('percent', 'Salary %'),
        ('days', 'Days'),
    ])
    address_id = fields.Many2many(
        'res.partner', string="Job Location",
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        help="Address where employees are working")
    all_request_count = fields.Integer(compute='_compute_all_request_count', string="All Request Count")
    resource_id = fields.Many2one('request.resource', string='Request Resource')

    def _compute_all_request_count(self):
        for job in self:
            job.all_request_count = self.env['hiring.request'].sudo().search_count([('job_id', '=', job.id)])

    def _compute_current_pipeline(self):
        for rec in self:
            rec.current_pipeline = self.env['hr.applicant'].search_count(
                [('job_id', '=', rec.id), ('stage_id.is_accept', '=', True)])

    def _send_notification(self, state, partners):
        message = _('Job Position: %s is %s, Please approve') % (str(self.name), state)
        return self.message_post(body=message, partner_ids=partners)

    def action_hr_approve(self):
        group = self.env.ref('surgi_recruitment_management.group_gm_approve_job').sudo().users
        partners = []
        if group:
            for usr in group:
                partners.append(usr.partner_id.id)
            self._send_notification('HR approved', partners)
        self.write({
            'job_state': 'hr'})

    def action_hr_approve_multi(self):
        items = self.env['hr.job'].browse(self._context.get('active_ids', []))
        for item in items.filtered(lambda m: m.job_state == 'draft'):
            item.action_hr_approve()

    def action_create_request(self):
        for rec in self:
            request = self.env['hiring.request'].sudo().create(
                {
                    'active': True,
                    'job_id': rec.id,
                    'replacement_period': rec.replacement_period,
                    'department_id': rec.department_id.id,
                    'grade_id': rec.grade_id.id,
                    'resource_id': rec.resource_id.id,
                    'request_count': rec.no_of_recruitment,
                    'request_reason': 'manpower',
                    'address_id': [(6, 0, rec.address_id.ids)]})

    def action_create_request_multi(self):
        items = self.env['hr.job'].browse(self._context.get('active_ids', []))
        for item in items.filtered(lambda m: m.job_state == 'gm'):
            item.action_create_request()

    def action_gm_approve(self):
        self.ensure_one()
        self.write({
            'job_state': 'gm'
        })

    def action_gm_approve_multi(self):
        items = self.env['hr.job'].browse(self._context.get('active_ids', []))
        for item in items.filtered(lambda m: m.job_state == 'hr'):
            item.action_gm_approve()

    def show_requests(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Hiring Requests',
            'view_mode': 'tree,form',
            'res_model': 'hiring.request',
            'domain': [('job_id', '=', self.id)],
        }

    @api.model
    def create(self, values):
        for rec in self:
            group = self.env.ref('surgi_recruitment_management.group_hr_approve_job').sudo().users
            partners = []
            if group:
                for usr in group:
                    partners.append(usr.partner_id.id)
                self._send_notification('created', partners)
        return super().create(values)
