# -*- coding: utf-8 -*-
{
    'name': "surgi_manager_reports",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','surgi_operation','sale','account','crm','sales_team','sale_crm','hr_expense'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'security/manager_security.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/customer_inv.xml',
        'views/sales_line_manteam.xml',
        'views/hr_expance.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
