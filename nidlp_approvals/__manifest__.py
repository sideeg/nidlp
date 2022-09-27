{
    "name": "nidlp_approvals",
    "summary": """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",
    "description": """
        Long description of module's purpose
    """,
    "author": "Odoo-PS",
    "website": "https://www.odoo.com",
    "category": "Uncategorized",
    "version": "0.1",
    "depends": ["nidlp_hr", "hr_expense"],
    # always loaded
    "data": [
        "data/approval_category_data.xml",
        "security/ir.model.access.csv",
        "data/data.xml",
        "security/record_rules.xml",
        "views/views.xml",
        "report/trip_report.xml"
    ],
}
