# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo
#    Copyright (C) 2021 dev:Mohamed Saber.
#    E-Mail:mohamedabosaber94@gmail.com
#    Mobile:+201153909418
#
##############################################################################
{
    'name': "Surgi Recruitment Management",
    'summary': """Custom HR Recruitment""",
    'description': """Custom HR Recruitment:
    -Hiring Request Form
    -Interview Process Setup
    -Customization in Job Position
    -Resource Setup
    -Customization in Application and Survey
    -
    """,
    'author': "Mohamed Saber",
    'category': 'Recruitment',
    'version': '14.1',
    'license': 'AGPL-3',
    # any module necessary for this one to work correctly

    'depends': ['base','mail','hr','portal','hr_recruitment','surgi_hr_payroll','survey','hr_recruitment_survey','hr_contract'],

    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'data/email_templates.xml',
        'views/calendar_event.xml',
        'views/hr_job_view.xml',
        'views/resource_view.xml',
        'views/hiring_request_view.xml',
        'views/hr_recruitment_stage.xml',
        'views/interview_process_view.xml',
        'views/hr_applicant.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}
