# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'purchase contract',
    'version' : '1.1',
    'summary': 'purchase & contract',
    'sequence': 10,
    'description': """ """,
    'category': 'Accounting/Accounting',

    'depends' : ['purchase'],
    'data': [
        #'security/account_security.xml',
        #'security/ir.model.access.csv',
        'data/service_cron.xml',
        'views/purchase_order_form_inherited.xml',
    ],
    'demo': [    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
