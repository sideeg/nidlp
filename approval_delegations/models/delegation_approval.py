from odoo import api, fields, models

class ApprovalCategory(models.Model):
    _inherit = "employee.delegations"
    _description = ""

    delegate_request_approval = fields.Boolean('delegate_request_approval',default=False)

    def access_returned(self):
        super().access_returned()
        for rec in self:
            if rec.delegate_request_approval :
                aproval_id = self.env["approval.category"].search([('user_id', '=', rec.delegated_employee_id)])
                aproval_id.user_id = rec.employee_id
                rec.delegate_request_approval = False

