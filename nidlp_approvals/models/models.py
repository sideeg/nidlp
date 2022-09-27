from odoo import _, api, fields, models
from odoo.exceptions import AccessError, UserError, ValidationError


class ApprovalLevel(models.Model):
    _name = "approval.category.levels"
    _order = "sequence, id"

    name = fields.Char()
    type = fields.Selection(
        [
            ("group", "Group"),
            ("sector_manager", "Sector Managers"),
            ("department_manager", "Department Managers"),
            ("line_manager", "Line Managers"),
            ("user", "Certain User"),
        ]
    )
    is_transfer = fields.Boolean("New Department/Sector")
    user_id = fields.Many2one("res.users")
    group_id = fields.Many2one("res.groups", string="Group")
    sequence = fields.Integer("Sequence")
    category_id = fields.Many2one("approval.category")


# class NewModule(models.Model):
#     _name = 'new_module.new_module'
#     _inherit = 'new_module.new_module'
#
#     name = fields.Char()
