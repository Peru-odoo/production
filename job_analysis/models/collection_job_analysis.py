# -*- coding: utf-8 -*-
import datetime

from odoo import models, fields, api, _
import odoo.addons.decimal_precision as dp
from odoo.exceptions import ValidationError, UserError


class CollectionJobAnalysis(models.Model):
    _name = 'collection.job.analysis'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Collection Job Analysis'
    _rec_name = 'position_id'

    batch_id = fields.Many2one('job.analysis.batch')
    active = fields.Boolean(string="Active", default=True)
    question_id = fields.Many2one('job.analysis.questionnaire')
    position_id = fields.Many2one(comodel_name="hr.job", string="Job Position")
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    answer_line_ids = fields.One2many('answer.line', 'collection_id')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('manager', 'Manager Approved'),('parent', 'Parent Manager Approved'),('hr', 'HR Manager Approved')
    ], string='Status', copy=False, index=True, readonly=True, default='draft')


    def manager_approve(self):
        self.ensure_one()
        self.write({'state': 'manager'})

    def parent_approve(self):
        self.ensure_one()
        self.write({'state': 'parent'})

    def hr_approve(self):
        self.ensure_one()
        self.write({'state': 'hr'})

    def reset(self):
        self.ensure_one()
        if self.state == 'manager':
            self.write({'state': 'draft'})
        elif self.state == 'parent':
            self.write({'state': 'manager'})
        elif self.state == 'hr':
            self.write({'state': 'parent'})

class AnswerLine(models.Model):
    _inherit = 'answer.line'

    collection_id = fields.Many2one('collection.job.analysis')
