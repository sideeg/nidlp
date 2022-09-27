from odoo import fields, models, tools


class ResUser(models.Model):
    _inherit = "res.users"

    subordinate_employee_ids = fields.Many2many("hr.employee", compute="_compute_subordinates")
    sector_id = fields.Many2one("hr.sector", related="employee_id.sector_id", related_sudo=False)

    def _compute_subordinates(self):
        for user in self:
            subordinate_ids = self.env["hr.employee"]
            if user.employee_id:
                subordinate_ids |= user.employee_id.subordinate_ids
                if user.employee_id == user.sector_id.manager_id:
                    subordinate_ids |= user.sector_id.employee_ids
                if user.employee_id == user.department_id.manager_id:
                    subordinate_ids |= user.department_id.member_ids
            user.subordinate_employee_ids = [(6, 0, subordinate_ids.ids)]
