from odoo import models, fields, api, _


class HrEmployee(models.Model):
    _inherit = 'hr.employee'


    def action_unfollow(self):
        pass



class HrhiringReq(models.Model):
    _inherit = 'hiring.request'

class Grade(models.Model):
    _inherit = 'grade.grade'
