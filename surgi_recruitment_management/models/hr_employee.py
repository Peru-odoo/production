from odoo import models, fields, api, _
from datetime import datetime, date
from datetime import datetime
from dateutil.relativedelta import relativedelta
from werkzeug.urls import url_join

class HRcontract(models.Model):
    _inherit = 'hr.contract'

    job_id = fields.Many2one('hr.job', compute='_compute_employee_contract', store=True, readonly=False,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id),('job_state','=','gm')]", string='Job Position')


class HREmployee(models.Model):
    _inherit = 'hr.employee'

    job_id = fields.Many2one('hr.job', "Job Position", domain="['|', ('company_id', '=', False), ('company_id', '=', company_id),('job_state','=','gm')]")


    def action_create_request(self):
        for rec in self:
            rec.active = False
            request = self.env['hiring.request'].create(
                {
                    'active': True,
                    'job_id': rec.job_id.id,
                    'replacement_period': rec.job_id.replacement_period,
                    'department_id': rec.job_id.department_id.id,
                    'grade_id': rec.job_id.grade_id.id,
                    'resource_id': rec.job_id.resource_id.id,
                    'request_count': rec.job_id.no_of_recruitment,
                    'request_reason': 'replacement',
                    'address_id': [(6, 0, rec.job_id.address_id.ids)]})
            return request

    def action_create_request_multi(self):
        items = self.env['hr.employee'].browse(self._context.get('active_ids', []))
        for item in items:
            item.action_create_request()
