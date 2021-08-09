from odoo import models, fields, api, _


class CalendarEvent(models.Model):
    _inherit = 'calendar.event'

    job_id = fields.Many2one('hr.job')
    applicant_id = fields.Many2one('hr.applicant')
    stage_id = fields.Many2one('hr.recruitment.stage')
    survey_ids = fields.Many2many('survey.survey')

    def action_sendmail(self):
        email = self.env.user.email
        if email:
            for meeting in self:
                if meeting.job_id:
                    meeting.attendee_ids._send_mail_to_attendees('surgi_recruitment_management.email_template_data_applicant_meeting',force_send=True)
                else:
                    meeting.attendee_ids._send_mail_to_attendees('calendar.calendar_template_meeting_invitation')
        return True
