from odoo import models, fields, api
from odoo.exceptions import ValidationError

class NewModule(models.Model):
    _name = 'helpdesk.category'
    _rec_name = 'name'
    _description = 'HelpDesk Category'

    name = fields.Text()

class HelpdeskTeamInherit(models.Model):
    _inherit = 'helpdesk.team'

    category_ids = fields.Many2many(comodel_name="helpdesk.category", string="Category", )
    category_needed = fields.Boolean(string="Category Needed", )
    is_maintenance = fields.Boolean(string="Equipment", )
    create_task = fields.Boolean(string="Create Task", )


class HelpdeskTicketInherit(models.Model):
    _inherit = 'helpdesk.ticket'
    category_id = fields.Many2one(comodel_name="helpdesk.category", string="Category", )
    is_user_manager = fields.Boolean(string="", compute='compute_is_user_manager')
    request_user_id = fields.Many2one(comodel_name="res.users",readonly=1 ,string="User Request",default=lambda self: self.env.user.id)
    is_manager_appoval = fields.Boolean(string="",  )
    other_request = fields.Boolean(string="",)
    new_other_request = fields.Boolean(string="",compute='get_all_other_request')
    type_helpdesk = fields.Selection(string="", selection=[('helpdesk', 'Help Desk'), ('maintenance_helpdesk', 'Maintenance HelpDesk'), ], required=False, )
    equipment_id = fields.Many2one(comodel_name="maintenance.equipment", string="Equipment", required=False, )
    state_repair = fields.Selection(string="Repair State", selection=[('Repaired', 'Repaired'), ('Not Repaired', 'Not Repaired'), ], required=False, )
    description_repair= fields.Text(string="Description", required=False, )
    delivery_expect_date = fields.Date(string="Delivery Expect Date", required=False, )
    is_state_repair = fields.Boolean(string="",  )
    create_task = fields.Boolean(string="Create Task",related='team_id.create_task' )
    category_needed = fields.Boolean(string="Category Needed",related='team_id.category_needed'  )
    is_maintenance = fields.Boolean(string="Maintenance",related='team_id.is_maintenance'  )
    appear_create_task = fields.Boolean(compute='compute_appear_create_task')

    def compute_appear_create_task(self):
        for rec in self:
            rec.appear_create_task=False
            if rec.env.user.id in rec.stage_id.other_request_ids.ids:
                rec.appear_create_task = True

    def button_create_task(self):

        self.env['project.task'].create({
            'name':self.name,
            'user_id':self.user_id.id,
        })

    @api.onchange('state_repair')
    def check_state_repair(self):
        if self.state_repair:
            self.is_state_repair=True
            self.description_repair=''

    @api.depends('stage_id')
    def get_all_other_request(self):
        statge_rec=self.env['helpdesk.stage']
        for rec in self:
            rec.new_other_request=False
            for req in statge_rec.search([('id', '!=', rec.stage_id.id)]):
                if req.sequence > self.stage_id.sequence and self.env.user.id in req.user_ids.ids:
                    rec.other_request = True
                    rec.new_other_request=True
                    break
                if req.sequence > rec.stage_id.sequence and self.env.user.id not in req.user_ids.ids:
                    rec.other_request = False
                    break
                else:
                    rec.other_request = False
                    break



    def button_manager_approval(self):
        self.is_manager_appoval=True


    @api.depends('request_user_id')
    def compute_is_user_manager(self):
        for rec in self:
            rec.is_user_manager = False
            if self.env.user.id==rec.request_user_id.employee_id.parent_id.user_id.id:
                rec.is_user_manager=True
            elif self.env.user.id==rec.request_user_id.employee_id.parent_id.parent_id.user_id.id:
                rec.is_user_manager=True
            elif self.env.user.id==rec.request_user_id.employee_id.parent_id.parent_id.parent_id.user_id.id:
                rec.is_user_manager=True
            elif self.env.user.id==rec.request_user_id.employee_id.parent_id.parent_id.parent_id.parent_id.user_id.id:
                rec.is_user_manager=True
            elif self.env.user.id==rec.request_user_id.employee_id.parent_id.parent_id.parent_id.parent_id.parent_id.user_id.id:
                rec.is_user_manager=True



    @api.onchange('stage_id')
    def constrain_stage_id(self):
        statges_list=[]
        statge_rec=self.env['helpdesk.stage']
        for rec in statge_rec.search([]):
            if self.team_id.id in rec.team_ids.ids:
                statges_list.append(int(rec.sequence))

        print(self.stage_id.sequence,'eeeeeeeeeeeeeee',statges_list)
        if statges_list:
            if self.env.user.id not in self.stage_id.user_ids.ids and self.team_id.id in self.stage_id.team_ids.ids:
                if int(self.stage_id.sequence) > int(min(statges_list)) :
                    raise ValidationError("Not Allowed User Access Has Not Permission Please Check User Stage")
            if self.is_manager_appoval==False and int(self.stage_id.sequence) > int(min(statges_list)):
                raise ValidationError("Not Allowed doesn't has Permission Only For Manager")

        else:
            raise ValidationError("Please Enter Stage Sequence")




    @api.onchange('team_id')
    def compute_category_ids(self):
        lines=[]
        if self.team_id.category_ids:
            for rec in self.team_id.category_ids:
                lines.append(rec.id)
        return {'domain': {'category_id': [('id', 'in',lines )]}}


class HelpdeskStageInherit(models.Model):
    _inherit = 'helpdesk.stage'

    user_ids = fields.Many2many(comodel_name="res.users", string="User", )
    other_request_ids = fields.Many2many(comodel_name="res.users", relation="other",
                                         column1="req1", column2="req2", string="Other Request", )
    all_users = fields.Boolean()

    @api.onchange('all_users')
    def get_all_users(self):
        users_list=[]
        for rec in self.env['res.users'].search([]):
            users_list.append(rec.id)
        if self.all_users:
            self.user_ids=[(6,0,users_list)]

        else:
            self.user_ids =False
