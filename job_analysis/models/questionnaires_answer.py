# -*- coding: utf-8 -*-
import datetime

from odoo import models, fields, api, _
import odoo.addons.decimal_precision as dp
from odoo.exceptions import ValidationError, UserError


class QuestionnairesAnswer(models.Model):
    _name = 'questionnaires.answer'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Questionnaires Answer'
    _rec_name = 'batch_id'

    batch_id = fields.Many2one('job.analysis.batch', readonly=True)
    from_date = fields.Date('Start', readonly=True)
    to_date = fields.Date('End', readonly=True)
    active = fields.Boolean(string="Active", default=True)
    employee_id = fields.Many2one(
        'hr.employee', string='Employee', readonly=True)
    manager_id = fields.Many2one(comodel_name="hr.employee", string="Manager", readonly=True,
                                 related='employee_id.parent_id')
    department_id = fields.Many2one(comodel_name="hr.department", string="Department", readonly=True,
                                    related='employee_id.department_id')
    position_id = fields.Many2one(comodel_name="hr.job", string="Position", readonly=True, related='employee_id.job_id')
    answer_line_ids = fields.One2many('answer.line', 'answer_id',tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirmed')
    ], string='Status', copy=False, index=True, readonly=True, default='draft',tracking=True)
    parent_manager_ids = fields.Many2many('res.users', string='Parent Managers', compute='_compute_parent_manager',
                                          store=True)

    @api.depends('manager_id')
    def _compute_parent_manager(self):
        for rec in self:
            record = rec.manager_id
            parents = []
            while record.parent_id.user_id:
                parents.append(record.parent_id.user_id.id)
                record = record.parent_id
            rec.parent_manager_ids = [pa for pa in parents if pa]

    def confirm(self):
        self.ensure_one()
        self.write({'state': 'confirm'})
        for line in self.answer_line_ids:
            if not line.row_answer_ids:
                raise ValidationError('Please add some answer to all question')
            line.send_collection()


    def reset(self):
        self.ensure_one()
        self.write({'state': 'draft'})


class AnswerLine(models.Model):
    _name = 'answer.line'

    question_id = fields.Many2one('job.analysis.questionnaire')
    row_answer_ids = fields.One2many('answer.row','answer_id')
    answer_id = fields.Many2one('questionnaires.answer')
    employee_id = fields.Many2one(
        'hr.employee', string='Employee', related='answer_id.employee_id', readonly=True,store=True)
    manager_id = fields.Many2one(comodel_name="hr.employee", string="Manager", readonly=True,
                                 related='employee_id.parent_id',store=True)
    department_id = fields.Many2one(comodel_name="hr.department", string="Department", readonly=True,
                                    related='employee_id.department_id',store=True)
    position_id = fields.Many2one(comodel_name="hr.job", string="Position", readonly=True, related='employee_id.job_id',store=True)
    batch_id = fields.Many2one(related='answer_id.batch_id', store=True)



    def send_collection(self):
        self.ensure_one()
        if not self.collection_id:
            collection = self.env['collection.job.analysis'].sudo().search(
                [('company_id', '=', self.env.user.company_id.id), ('batch_id', '=', self.batch_id.id),
                 ('position_id', '=', self.position_id.id)], limit=1)
            if collection:
                self.collection_id = collection.id






class Answer(models.Model):
    _name = 'answer.row'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']

    name = fields.Text('Employee Answer')
    collection_answer = fields.Text('Final Answer')
    answer_date = fields.Datetime()
    employee_id = fields.Many2one(
        'hr.employee', string='Employee', related='answer_id.employee_id', readonly=True)
    manager_id = fields.Many2one(comodel_name="hr.employee", string="Manager", readonly=True,
                                 related='employee_id.parent_id',store=True)
    department_id = fields.Many2one(comodel_name="hr.department", string="Department", readonly=True,
                                    related='employee_id.department_id',store=True)
    position_id = fields.Many2one(comodel_name="hr.job", string="Position", readonly=True, related='employee_id.job_id',store=True)
    question_id = fields.Many2one(related='answer_id.question_id', store=True)
    batch_id = fields.Many2one(related='answer_id.batch_id', store=True)
    manager_check = fields.Boolean('Manager Checker')
    parent_check = fields.Boolean('Parent Checker')
    hr_check = fields.Boolean('HR Checker')
    job_analysis_type_id = fields.Many2one('job.analysis.type', string='Job Analysis Type')
    answer_id = fields.Many2one('answer.line')
    is_manager = fields.Boolean(compute='_compute_groups')
    is_parent = fields.Boolean(compute='_compute_groups')
    is_hr = fields.Boolean(compute='_compute_groups')

    @api.onchange('name')
    def onchange_name_ans(self):
        if self.employee_id.user_id and self.employee_id.user_id.id == self.env.user.id:
            self.answer_date = fields.Datetime.today()
            self.collection_answer = self.name

    def _compute_groups(self):
        for rec in self:
            if self.env.user == rec.answer_id.manager_id.user_id and rec.answer_id.manager_id.user_id:
                rec.is_manager = True
            else:
                rec.is_manager = False
            if self.env.user in rec.answer_id.answer_id.parent_manager_ids and rec.answer_id.answer_id.parent_manager_ids:
                rec.is_parent = True
            else:
                rec.is_parent = False
            if self.env.user.has_group('job_analysis.group_job_analysis_manager'):
                rec.is_hr = True
            else:
                rec.is_hr = False



