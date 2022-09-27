from odoo import fields, models, tools


class HrContract(models.Model):
    _inherit = "hr.contract"
    housing_allowance = fields.Monetary()
    transportation_allowance = fields.Monetary()
    other_allowance = fields.Monetary()
    total_package = fields.Monetary(compute="_compute_total_package")
    phone_allowance = fields.Monetary()
    cost_living_allowance = fields.Monetary()
    leave_compensation_days = fields.Integer(string="Leave Compensation Days")
    salary_type_id = fields.Many2one('hr.contract.salary.type', 'Salary Type')

    def _compute_total_package(self):
        fields = [
            "l10n_sa_housing_allowance",
            "wage",
            "l10n_sa_transportation_allowance",
        ]
        for contract in self:
            contract.total_package = sum(contract[field] for field in fields)


class HrContractSalaryType(models.Model):
    _name = 'hr.contract.salary.type'
    _description = 'Hr Contract Salary Type'

    name = fields.Char()

    name = fields.Char()
