from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    employee_certificate_issuer = fields.Many2one(
        "hr.employee", related="company_id.employee_certificate_issuer", readonly=False
    )
    it_staff_ids = fields.Many2many("res.users", related="company_id.it_staff_ids", readonly=False)
    company_stamp = fields.Image(related="company_id.company_stamp", max_width=128, max_height=128, readonly=False)
    company_ceo = fields.Many2one("hr.employee", related="company_id.company_ceo", readonly=False)
