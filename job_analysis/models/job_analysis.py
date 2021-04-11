# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import odoo.addons.decimal_precision as dp
from odoo.exceptions import ValidationError, UserError


class JobAnalysisBatch(models.Model):
    _name = 'job.analysis.batch'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Job Analysis Batch'

    name = fields.Char()
    from_date = fields.Date('Start')
    to_date = fields.Date('End')
    active = fields.Boolean(string="Active", default=True)
    type = fields.Selection([
        ('employee', 'Employee'),
        ('company', 'Company'), ('tag', 'Employee Tag'), ('department', 'Department')
    ], string='Batch Type',required=1)
    employee_ids = fields.Many2many(
        'hr.employee', string='Employees')
    company_ids = fields.Many2many('res.company', string='Companies')
    category_ids = fields.Many2many('hr.employee.category', string='Employee Tags')
    department_ids = fields.Many2many('hr.department', string='Departments')
    user_id = fields.Many2one('res.users', string='Responsible', readonly=True, default=lambda self: self.env.user)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirmed')
    ], string='Status', copy=False, index=True, readonly=True, default='draft')
    questionnaire_ids = fields.Many2many('job.analysis.questionnaire')
    answer_count = fields.Integer("Registered", compute="_compute_answer_statistic")
    answer_done_count = fields.Integer("Attempts", compute="_compute_answer_statistic")

    def _compute_answer_statistic(self):
        for rec in self:
            rec.answer_count = self.env['questionnaires.answer'].sudo().search_count([('batch_id','=',self.id)])
            rec.answer_done_count = self.env['collection.job.analysis'].sudo().search_count([('batch_id','=',self.id)])


    def create_answer(self, employee_id):
        qust = []
        for q in self.questionnaire_ids:
            qust.append((0, 0, {'question_id': q.id}))
        answer = self.env['questionnaires.answer'].create(
            {'batch_id': self.id,
             'from_date': self.from_date,
             'to_date': self.to_date,
             'employee_id': employee_id.id,
             'answer_line_ids': qust})
        return answer

    def create_collection(self, position,question,company):
        collection = self.env['collection.job.analysis'].create(
            {'batch_id': self.id,
             'question_id': question.id,
             'position_id':position.id,
             'company_id':company.id})
        return collection

    def confirm(self):
        self.ensure_one()
        self.write({'state': 'confirm'})
        questions = self.questionnaire_ids
        if self.type == 'employee':
            positions = []
            for emp in self.employee_ids:
                self.create_answer(emp)
                positions.append(emp.job_id)
            for po in set(positions):
                for q in questions:
                    self.create_collection(po,q,self.company_id)
        elif self.type == 'company':
            for com in self.company_ids:
                positions = []
                employees = self.env['hr.employee'].sudo().search([('company_id','=',com.id)])
                for emp in employees:
                    self.create_answer(emp)
                    positions.append(emp.job_id)
                for po in set(positions):
                    for q in questions:
                        self.create_collection(po, q,com)
        elif self.type == 'tag':
            positions = []
            for tag in self.category_ids:
                employees = self.env['hr.employee'].sudo().search([('company_id','=',self.company_id.id),('category_ids','in',tag.id)])
                for emp in employees:
                    self.create_answer(emp)
                    positions.append(emp.job_id)
                for po in set(positions):
                    for q in questions:
                        self.create_collection(po, q, self.company_id)
        elif self.type == 'department':
            positions = []
            for deb in self.department_ids:
                employees = self.env['hr.employee'].sudo().search([('company_id','=',self.company_id.id),('department_id','=',deb.id)])
                for emp in employees:
                    self.create_answer(emp)
                    positions.append(emp.job_id)
                for po in set(positions):
                    for q in questions:
                        self.create_collection(po, q, self.company_id)
        return True

    def show_questionnaires(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Registered',
            'view_mode': 'tree,form',
            'res_model': 'questionnaires.answer',
            'domain': [('batch_id', '=', self.id)],
            'context': "{'create': False}"
        }

    def show_answer(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Answer Collections',
            'view_mode': 'tree,form',
            'res_model': 'collection.job.analysis',
            'domain': [('batch_id', '=', self.id)],
            'context': "{'search_default_position': 1,'search_default_question': 1,'create': False}"
        }