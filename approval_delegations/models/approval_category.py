from odoo import api, fields, models
from datetime import datetime

class ApprovalCategory(models.Model):
    _inherit = "approval.category"
    _description = ""


    def write(self, vals):
        print(vals.get('approver_ids'),'//////////////////////////////////////////////////////////////////////////')
        if vals.get('approver_ids') is None :
            return super().write(vals)
        for count,i in enumerate(vals.get('approver_ids')):
            if i[0] == 2:
                pass # the user is deleted
                print(i, '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

            elif i[0] == 0 :
                pass # the user is added
                employee_delegations = self.env["employee.delegations"].search([('employee_id', '=', i[-1].get('user_id'))])
                employee_delegations.delegate_request_approval = True
                print(count,'+++++++++9999999999999999999999999999999999999999999999999999999999999')
                vals['approver_ids'][count][-1]['user_id'] = employee_delegations.delegated_employee_id.id if employee_delegations.delegated_employee_id.id and employee_delegations.date_to < datetime.now()  else vals['approver_ids'][count][-1]['user_id']


        return super().write(vals)

