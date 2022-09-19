
from odoo import fields, models, api
from datetime import datetime

class HrLeave(models.Model):
    _inherit = 'hr.leave'
    # delegations_id = fields.Many2one('employee.delegations')
    delegations_employee_id = fields.Many2one('hr.employee', 'delegations')

    def action_approve(self):
        # super(HrLeave, self).action_approve()
        super().action_approve()

        for rec in self :
            delegations_info = {'employee_id':self.env.user.employee_id.id,'delegated_employee_id':rec.delegations_employee_id.id,
                                'date_from':rec.date_from,'date_to':rec.date_to,'state':'draft','name':'test','date':datetime.now(),}
            filed = self.env['employee.delegations'].create(delegations_info)
            print(filed,'//////////////////////////////////////////////////////////////////////')
            filed.onchange_method()
            filed.access_granted()

