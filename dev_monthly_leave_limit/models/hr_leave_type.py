# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle
#
##############################################################################

from datetime import datetime, timedelta
from odoo import api, fields, models,_
from odoo.exceptions import ValidationError




class HrLeaveType(models.Model):
    _inherit = 'hr.leave.type'

    flag_monthly_limit = fields.Boolean(string="Monthly Leave Limit")
    leave_limit_days = fields.Float(string="Leave Limit Days")

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:



class HrLeaveTypes(models.Model):
    _inherit = 'hr.leave.type'

    limited_hours = fields.Boolean(string="Limited Hours",  )
    mini_hours = fields.Float(string="Mini Hours",  required=False, )
    max_hours = fields.Float(string="Max Hours",  required=False, )

    @api.constrains('mini_hours','max_hours')
    def prevent_mini_max_hours(self):

        if self.limited_hours:
            if self.mini_hours>self.max_hours:
                raise ValidationError(_('Minimum hours Must be less than Maximum hours'))
