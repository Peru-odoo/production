from odoo import models, fields, api, _
from datetime import datetime, date
from datetime import datetime
from dateutil.relativedelta import relativedelta
from werkzeug.urls import url_join
from odoo.exceptions import UserError
from odoo.tools import formataddr


class HRApplicant(models.Model):
    _inherit = 'hr.applicant'

    number = fields.Char()

    line_ids = fields.One2many('applicant.process.line', 'applicant_id')
    job_id = fields.Many2one('hr.job', "Applied Job",
                             domain="['|', ('company_id', '=', False), ('company_id', '=', company_id),('job_state','=','gm')]",
                             tracking=True)
    interview_state = fields.Selection([
        ('accepted', 'Accepted'),
        ('rejected ', 'Rejected'),
        ('shortlisted ', 'Shortlisted')
    ], string='Interview Status')

    @api.onchange('job_id')
    @api.constrains('job_id')
    def onchange_job_id(self):
        if self.job_id:
            self.line_ids.unlink()
            last = self.env['applicant.survey.line'].search([('applicant_id', '=', self.id)]).unlink()
            setup = self.env['interview.process'].search([('job_ids', '=', self.job_id.id)], limit=1)
            if setup:
                new_partner_id = self.env['res.partner'].search([('email','=',self.email_from)], limit=1)
                if not new_partner_id:
                    new_partner_id = self.env['res.partner'].create({
                        'is_company': False,
                        'type': 'private',
                        'name': self.partner_name,
                        'email': self.email_from,
                        'phone': self.partner_phone,
                        'mobile': self.partner_mobile
                    })
                self.partner_id = new_partner_id.id
                for line in setup.line_ids:
                    process_line_id = self.env['applicant.process.line'].create({
                        'name': line.name,
                        'stage_id': line.stage_id.id,
                        'user_id': line.user_id.id,
                        'survey_ids': line.survey_ids.ids,
                        'applicant_survey_ids':line.applicant_survey_ids.ids,
                        'applicant_id': self.id,
                        'reviewer_ids': line.reviewer_ids.ids,
                        'type': line.type})
                    users = [x.id for x in line.reviewer_ids]
                    for su in line.survey_ids:
                        users.append(line.user_id.id)
                        self.env['applicant.survey.line'].create({'survey_id': su.id,
                                                                  'partner_id': line.user_id.partner_id.id,
                                                                  'applicant_id': self.id,
                                                                  'user_ids': users,
                                                                  'stage_id': line.stage_id.id,
                                                                  'process_line_id': process_line_id.id})
                    for sur in line.applicant_survey_ids:
                        self.env['applicant.survey.line'].create({'survey_id': sur.id,
                                                                  'partner_id': new_partner_id.id,
                                                                  'applicant_id': self.id,
                                                                  'stage_id': line.stage_id.id,
                                                                  'process_line_id': process_line_id.id})

    @api.model
    def create(self, values):
        values['number'] = self.env['ir.sequence'].next_by_code('hr.applicant') or '/'
        return super().create(values)

    def show_surveys(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Interview Surveys',
            'view_mode': 'tree',
            'res_model': 'applicant.survey.line',
            'domain': [('applicant_id', '=', self.id)],
        }

    def action_makeMeeting(self):
        res = super(HRApplicant, self).action_makeMeeting()
        survey_ids = self.line_ids.filtered(lambda m: m.stage_id == self.stage_id.id).mapped('applicant_survey_ids')
        partners = []
        partners.extend([self.partner_id.id,self.user_id.partner_id.id])
        if self.line_ids:
            for line in self.line_ids:
                partners.append(line.user_id.partner_id.id)
        res['context'].update({
            'default_partner_ids': partners,
            'default_job_id': self.job_id.id,
            'default_applicant_id': self.id,
            'default_stage_id':self.stage_id.id,
            'default_survey_ids': survey_ids.ids if survey_ids else [],
        })
        return res


class ApplicantProcessLine(models.Model):
    _name = 'applicant.process.line'



    name = fields.Char('Sequence')
    stage_id = fields.Many2one('hr.recruitment.stage')
    user_id = fields.Many2one('res.users', string='Interviewer')
    survey_ids = fields.Many2many('survey.survey', 'applicant_process_line_rel', 'process_line_id', 'survey_id',
                                  string='Recruiter Surveys')
    applicant_survey_ids = fields.Many2many('survey.survey', string='Applicant Surveys')
    accepted = fields.Boolean()
    rejected = fields.Boolean()
    shortlisted = fields.Boolean()
    applicant_id = fields.Many2one('hr.applicant')
    type = fields.Selection([
        ('zoom', 'Zoom'),
        ('physically ', 'Physically')
    ], string='Interview Type')
    reviewer_ids = fields.Many2many('res.users', string='Reviewers')

    def update_lines(self):
        self.env['applicant.survey.line'].search([('process_line_id', '=', self.id)]).unlink()
        for line in self:
            users = [x.id for x in line.reviewer_ids]
            for su in line.survey_ids:
                users.append(line.user_id.id)
                self.env['applicant.survey.line'].create({'survey_id': su.id,
                                                          'partner_id': line.user_id.partner_id.id,
                                                          'applicant_id': self.id,
                                                          'user_ids': users,
                                                          'stage_id':line.stage_id.id,
                                                          'process_line_id': line.id})
            for sur in line.applicant_survey_ids:
                self.env['applicant.survey.line'].create({'survey_id': sur.id,
                                                          'partner_id': line.applicant_id.partner_id.id,
                                                          'applicant_id': self.id,
                                                          'stage_id': line.stage_id.id,
                                                          'process_line_id': line.id})
    def write(self, values):
        res = super().write(values)
        if 'user_id' in values:
            self.update_lines()
        if 'survey_ids' in values:
            self.update_lines()
        if 'applicant_survey_ids' in values:
            self.update_lines()
        if 'reviewer_ids' in values:
            self.update_lines()
        return res



class ApplicantSurveyLine(models.Model):
    _name = 'applicant.survey.line'

    applicant_id = fields.Many2one('hr.applicant')
    process_line_id = fields.Many2one('applicant.process.line')
    stage_id = fields.Many2one('hr.recruitment.stage')
    job_id = fields.Many2one(related='applicant_id.job_id')
    user_ids = fields.Many2many('res.users')
    department_id = fields.Many2one(related='applicant_id.department_id')
    survey_id = fields.Many2one('survey.survey', string="Survey")
    response_id = fields.Many2one('survey.user_input', "Response", ondelete="set null")
    response_date = fields.Datetime(related='response_id.create_date')
    meeting_date = fields.Datetime(compute='_compute_meeting_date')
    state = fields.Selection(related='response_id.state')
    scoring_percentage = fields.Float(related='response_id.scoring_percentage', store=True)  # stored for perf reasons
    scoring_total = fields.Float(related='response_id.scoring_total', store=True)  # stored for perf reasons
    scoring_success = fields.Boolean(related='response_id.scoring_success', store=True)  # stored for perf reasons
    partner_id = fields.Many2one('res.partner')

    @api.depends('applicant_id', 'stage_id')
    def _compute_meeting_date(self):
        for rec in self:
            event = self.env['calendar.event'].search(
                [('applicant_id', '=', rec.applicant_id.id), ('stage_id', '=', rec.stage_id.id)], limit=1)
            if event:
                rec.meeting_date = event.start
            else:
                rec.meeting_date = False

    def action_start_survey(self):
        self.ensure_one()
        # create a response and link it to this applicant
        if not self.response_id:
            response = self.survey_id._create_answer(partner=self.partner_id)
            self.response_id = response.id
        else:
            response = self.response_id
        # grab the token of the response and start surveying
        return self.survey_id.action_start_survey(answer=response)

    def action_print_survey(self):
        """ If response is available then print this response otherwise print survey form (print template of the survey) """
        self.ensure_one()
        return self.survey_id.action_print_survey(answer=self.response_id)
