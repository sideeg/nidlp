from odoo import SUPERUSER_ID, _, api, fields, models
from odoo.exceptions import Warning


class res_company(models.Model):
    _inherit = "res.company"

    employee_certificate_issuer = fields.Many2one("hr.employee", "Employee Certificate Issuer")
    it_staff_ids = fields.Many2many("res.users", "it_staff_company_rel")
    company_stamp = fields.Image()
    company_ceo = fields.Many2one("hr.employee")
