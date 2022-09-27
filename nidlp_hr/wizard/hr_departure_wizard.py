# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class HrDepartureWizard(models.TransientModel):
    _inherit = "hr.departure.wizard"

    leave_compensation_days = fields.Integer(string="Leave Compensation Days", required=True)

    def action_register_departure(self):
        res = super(HrDepartureWizard, self).action_register_departure()
        if current_contract := self.employee_id.contract_id:
            current_contract.write({"leave_compensation_days": self.leave_compensation_days})
        return res
