from odoo import api, fields, models, tools

CATEGORY_SELECTION = [("required", "Required"), ("optional", "Optional"), ("no", "None")]


class ApprovalCategory(models.Model):
    _inherit = "approval.category"

    has_beneficiary = fields.Selection(
        CATEGORY_SELECTION, string="Has Adding Beneficiary ", default="no", required=True
    )
    is_employee_certificate = fields.Boolean(string="Employee Certificate Category")
    approval_levels = fields.One2many("approval.category.levels", "category_id")
    approval_level_type = fields.Selection(
        [("single", "Single Level Approval"), ("multi", "Multi-Level Approval")], default="single", required=True
    )
    is_change_department = fields.Boolean(string="Has Change of Department", default=False, required=True)
    is_change_sector = fields.Boolean(string="Has Change of Sector", default=False, required=True)

    is_change_housing_allowance = fields.Boolean(string="Has Change of housing allowance", default=False, required=True)
    is_change_transportation_allowance = fields.Boolean(
        string="Has Change of transportation allowance", default=False, required=True
    )
    is_change_other_allowance = fields.Boolean(string="Has Change of other allowance", default=False, required=True)
    is_change_wage = fields.Boolean(string="Has Change of basic salary", default=False, required=True)
    is_change_job_title = fields.Boolean(string="Has Change of Job Title", default=False, required=True)
    is_self_serving = fields.Boolean(default=True)
    is_change_status = fields.Boolean()
    has_distance_riyadh = fields.Selection(
        CATEGORY_SELECTION, string="Has Distance from riyadh", default="no", required=True
    )
    has_country = fields.Selection(CATEGORY_SELECTION, string="Has country", default="no", required=True)
    has_employee_class = fields.Selection(CATEGORY_SELECTION, string="Has employee class", default="no", required=True)
    has_external_stipend = fields.Selection(
        CATEGORY_SELECTION, string="Has external stipend", default="no", required=True
    )
    has_internal_stipend = fields.Selection(
        CATEGORY_SELECTION, string="Has internal stipend", default="no", required=True
    )
    is_trip = fields.Boolean()
    is_internal_trip = fields.Boolean()
    is_external_trip = fields.Boolean()

    expenses_product_id = fields.Many2one('product.product', 'Expenses Product')
    leave_type_id = fields.Many2one('hr.leave.type', 'Leave Type')
    template_id = fields.Many2one(
        'mail.template', 'Trip template', index=True,
        domain="[('model', '=', 'approval.request')]"
    )
    partner_e_id = fields.Many2one('res.partner', 'Travel agency')
