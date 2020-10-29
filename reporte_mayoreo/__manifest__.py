# -*- coding: utf-8 -*-
{
    'name': "reporte_mayoreo",
    'description': """
        Long description of module's purpose
    """,

    'author': "Raul Rolando Jardinot Gonzalez",
    'website': "http://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base','sale','report_xlsx','sol_pricelist'],

    'data': [
        # 'security/ir.model.access.csv',
        'views/pricelist_report.xml',
        'wizard/wizard_excel.xml',
        'report/report_sale_order.xml',
    ],

    'demo': [
        'demo/demo.xml',
    ],
}