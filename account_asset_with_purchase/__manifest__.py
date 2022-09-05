# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'account asset with purchase related',
    'version' : '1.1',
    'summary': 'account & asset',
    'sequence': 0,
    'description': """ """,
    'category': 'Accounting/Accounting',

    'depends' : ['purchase','account_accountant','account_asset'],
    'data': [
        'views/view_account_asset_purchase_tree.xml',
    ],
    'demo': [    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
