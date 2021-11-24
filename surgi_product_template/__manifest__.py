# -*- coding: utf-8 -*-
{
    'name': "SURGI Fileds Modify",

    'summary': """
        """,

    'description': """
        Long description of module's purpose
    """,

    'author': "SURGI-TECH",
    'website': "http://www.surgitech.net",


    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base','product'],

    'data': [
        'security/ir.model.access.csv',

        'views/product_template_view.xml',
    ],
    # "pre_init_hook": "pre_init_product_code",
}