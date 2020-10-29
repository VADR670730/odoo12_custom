# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Partner Custom',
    'version': '1.0',
    'summary': 'Partner Custom',
    'author': "SoftwareEscarlata",
    'description': """
    
  """,

    'category': 'sale',
    'depends': ['sale'],
    'data': [
        'views/res_partner.xml',
        'security/ir.model.access.csv',
    ],
}
