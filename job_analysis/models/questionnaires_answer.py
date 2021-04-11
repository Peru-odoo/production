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
    # child_ids = fields.One2many('hr.employee', 'parent_id', string='Direct subordinates')
    manager_id = fields.Many2one(comodel_name="hr.employee", string="Manager", readonly=True,
                                 related='employee_id.parent_id')
    department_id = fields.Many2one(comodel_name="hr.department", string="Department", readonly=True,
                                    related='employee_id.department_id')
    position_id = fields.Many2one(comodel_name="hr.job", string="Position", readonly=True, related='employee_id.job_id')
    answer_line_ids = fields.One2many('answer.line', 'answer_id')


class AnswerLine(models.Model):
    _name = 'answer.line'

    question_id = fields.Many2one('job.analysis.questionnaire')
    row_answer = fields.Text()
    answer_date = fields.Datetime()
    manager_check = fields.Boolean('Manager')
    parent_check = fields.Boolean('Parent')
    hr_check = fields.Boolean('HR')
    job_analysis_type_id = fields.Many2one('job.analysis.type', string='Job Analysis Type')
    answer_id = fields.Many2one('questionnaires.answer')
    employee_id = fields.Many2one(
        'hr.employee', string='Employee', related='answer_id.employee_id', readonly=True)
    manager_id = fields.Many2one(comodel_name="hr.employee", string="Manager", readonly=True,
                                 related='employee_id.parent_id')
    department_id = fields.Many2one(comodel_name="hr.department", string="Department", readonly=True,
                                    related='employee_id.department_id')
    position_id = fields.Many2one(comodel_name="hr.job", string="Position", readonly=True, related='employee_id.job_id')

    batch_id = fields.Many2one(related='answer_id.batch_id', store=True)

    @api.onchange('row_answer')
    @api.constrains('row_answer')
    def onchange_answer_date(self):
        if self.row_answer and self.employee_id.user_id and self.employee_id.user_id.id == self.env.user.id:
            self.answer_date = fields.Datetime.today()
            if not self.collection_id:
                collection = self.env['collection.job.analysis'].sudo().search(
                    [('company_id', '=', self.env.user.company_id.id), ('batch_id', '=', self.batch_id.id),
                     ('question_id', '=', self.question_id.id), ('position_id', '=', self.position_id.id)], limit=1)
                if collection:
                    self.collection_id = collection.id
