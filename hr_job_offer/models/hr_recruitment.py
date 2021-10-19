from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class HRRecruitment(models.Model):
    _inherit = 'hr.applicant'

    job_offer_id = fields.Many2one('hr.job.offer')
    is_hiring_approved = fields.Boolean(compute='_compute_is_hiring_approved')
    offering_date = fields.Date(related='job_offer_id.date', store=True)
    offering_state = fields.Selection(related='job_offer_id.state', store=True)


    def _compute_is_hiring_approved(self):
        for rec in self:
            if rec.hiring_approval_id:
                if rec.hiring_approval_id.state == 'gm':
                    rec.is_hiring_approved = True
                else:
                    rec.is_hiring_approved = False
            else:
                rec.is_hiring_approved = False

    def action_show_job_offer(self):
        self.ensure_one()
        offer = self.job_offer_id
        action = {
            'name': _('Job Offer'),
            'view_mode': 'form,tree',
            'res_model': 'hr.job.offer',
            'type': 'ir.actions.act_window',
            'context': {'form_view_initial_mode': 'readonly'},
            'res_id': offer.id,
        }
        return action
