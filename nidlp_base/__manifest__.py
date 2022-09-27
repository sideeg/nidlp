{
    "name": "nidlp_base",
    "summary": """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",
    "description": """
        Long description of module's purpose
    """,
    "author": "Odoo-PS",
    "website": "http://www.Odoo.com",
    "category": "Uncategorized",
    "version": "0.1",
    "data": [
        "reports/base_reports.xml",
        "data/groups.xml",
        "views/views.xml",
    ],
    "depends": ["mail", "hr_holidays", "hr_payroll", "approvals", "l10n_sa_hr_payroll", "sign"],
    "assets": {
        "web.assets_backend": [
            "nidlp_base/static/src/**/*",
        ],
    },
}
