# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Only view Created Contacts',
    'version': '1.0',
    'summary': 'Only view Created Contacts',
    'author': "SoftwareEscarlata",
    'description': """
    This Module allows only the contacts created by the logged-in user to be seen. It applies to sales, Inventory, CRM, etc.
The group with administrator role can see all the contacts
  """,

    'category': 'sale',
    'depends': ['sale'],
    'data': [
        'views/res_partner.xml',
        'security/ir.model.access.csv',
    ],
}
