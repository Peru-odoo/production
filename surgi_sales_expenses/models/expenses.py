from odoo import models, fields, api
from datetime import date,datetime,time,timedelta
from dateutil.relativedelta import relativedelta

class HrExpensesExpenses(models.Model):
    _name = 'hr.expenses.expenses'
    _rec_name = 'expensescc_id'

    expensescc_id = fields.Many2one(comodel_name="hr.expense", string="Expenses",)
    date = fields.Date(string="Date", required=False, )
    total_amount = fields.Float(string="Total Amount",  required=False, )
    expen_id = fields.Many2one(comodel_name="hr.expense", string="", required=False, )




class HRExpensesInherit(models.Model):
    _inherit = 'hr.expense'

    sales_id = fields.Many2one(comodel_name="operation.operation", string="Operation",)
    is_sales = fields.Boolean(string="IS Sales",related='product_id.is_sales_order'  )
    sales_state = fields.Char(string="Sales State",compute='compute_sales_state')
    # expenses_ids = fields.Many2many(comodel_name="hr.expense", relation="expenses_relation", column1="expenses_col1", column2="expenses_col2", string="Expenses",)
    expenses_lines_ids = fields.One2many(comodel_name="hr.expenses.expenses", inverse_name="expen_id", string="", required=False, )
    is_expenses_ids = fields.Boolean(string="",compute='filter_sales_id'  )

    partner_surgeon_id = fields.Many2one(comodel_name="res.partner", string="Surgeon")
    event_id = fields.Many2one(comodel_name="hr.expenses.event", string="Event", )
    sale_order_mandatory = fields.Boolean(string="Sale Order Mandatory",related='product_id.property_account_expense_id.sale_order_mandatory')

    total_expense_amount = fields.Float(string="Total Amount",compute='compute_total_expense_amount')

    num_day_expire = fields.Integer(compute='compute_num_day_expire' )

    def compute_num_day_expire(self):
        expiration_rec = self.env['hr.expense.expiration'].search([],limit=1)
        for rec in self:
            rec.num_day_expire=expiration_rec.num_day_expire
            if rec.num_day_expire:

                rec.filter_value_sales()

    @api.depends('sales_id','expenses_lines_ids')
    def compute_total_expense_amount(self):
        for rec in self:
            total_expense_amount=0.0
            for line in rec.expenses_lines_ids:
                total_expense_amount+=line.total_amount
            rec.total_expense_amount=total_expense_amount
    @api.depends('sales_id')
    def compute_sales_state(self):
        for rec in self:
            rec.sales_state=''
            if rec.sales_id:
                rec.sales_state =rec.sales_id.state



    @api.onchange('name','date','sales_id')
    def filter_value_sales(self):
        sales_list=[]
        today_date = datetime.strptime(str(date.today()), '%Y-%m-%d').date()
        operation_rec = self.env['operation.operation'].search([])
        expiration_rec = self.env['hr.expense.expiration'].search([],limit=1)
        for rec in operation_rec:
            if rec.start_datetime:
                date_order = datetime.strptime(str(rec.start_datetime).split(".")[0],
                                                      '%Y-%m-%d %H:%M:%S').date()

                if expiration_rec and int(str((today_date - date_order).days))<=expiration_rec.num_day_expire:
                    sales_list.append(rec.id)
        return {
            'domain': {'sales_id': [('id', 'in',sales_list )]}
        }

    @api.depends('sales_id')
    def filter_sales_id(self):
        for expen in self:
            line_list = [(5,0,0)]
            expen.is_expenses_ids=False
            for rec in self.search([]):
                if expen._origin.id !=rec.id and expen.sales_id.id==rec.sales_id.id:
                    line_list.append((0,0,{
                        'expensescc_id': rec.id,
                        'date': rec.date,
                        'total_amount': rec.total_amount,
                    }))
                    expen.is_expenses_ids=True
            if expen.sales_id and line_list:
                expen.update({'expenses_lines_ids':line_list})
            else:
                expen.expenses_lines_ids=False

    @api.onchange('employee_id','product_id')
    def filter_product_id(self):
        product_list=[]

        for rec in self.env['product.product'].search([('can_be_expensed', '=', True)]):
            if self.employee_id.department_id.id in rec.department_ids.ids:
                product_list.append(rec.id)

        return {
            'domain': {'product_id': [('id', 'in', product_list)]}
        }

class HrExpenseSheetInherit(models.Model):
    _inherit = 'hr.expense.sheet'

    account_reviewed= fields.Boolean(string="Account Reviewed",  )
    treasury_manager= fields.Boolean(string="Treasury Manager",  )


    def button_account_reviewed(self):
        self.account_reviewed=True
    def button_treasury_manager(self):
        self.treasury_manager=True

    def action_sheet_move_create(self):
        res=super(HrExpenseSheetInherit, self).action_sheet_move_create()
        if self.account_move_id:
            self.account_move_id.date=date.today()
        return res

class AccountAccountInherit(models.Model):
    _inherit = 'account.account'

    sale_order_mandatory = fields.Boolean(string="Sale Order Mandatory",  )
