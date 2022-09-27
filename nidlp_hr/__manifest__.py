{
    "name": "nidlp_hr",
    "summary": """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",
    "description": """
        Long description of module's purpose
    """,
    "author": "Odoo-ps",
    "website": "http://www.yourcompany.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Uncategorized",
    "version": "0.1",
    "depends": ["nidlp_base"],
    # always loaded
    "data": [
        "views/res_settings.xml",
        "views/hr_contract_views.xml",
        "views/hr_employee_views.xml",
        "views/hr_leave_type.xml",
        "reports/hr_salary_report.xml",
        "reports/hr_salary_transfer.xml",
        "views/actions.xml",
        "data/email_template.xml",
        "security/ir.model.access.csv",
        "wizard/hr_departure_wizard.xml",
        "reports/hr_wps_report.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "nidlp_hr/static/src/js/hr.js",
        ],
        "web.assets_qweb": [
            "nidlp_hr/static/src/xml/payslip_template.xml",
        ],
    },
}
