
from odoo import fields, models, api
from datetime import datetime
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools.translate import _



class HrLeave(models.Model):
    _inherit = 'hr.leave'
    # delegations_id = fields.Many2one('employee.delegations')
    delegations_employee_id = fields.Many2one('hr.employee', 'delegations')

    def action_approve(self):

            # group_e.write({'users': [(1, self.env.user.id)]})

        super().action_approve()

        for rec in self :
            is_leave_user_test = rec.user_has_groups('hr_holidays.group_hr_holidays_user')
            if is_leave_user_test:
                print(is_leave_user_test, '//////////////////////////////////////////////////////////////////////')

                group_e = self.env.ref('hr_holidays.group_hr_holidays_user', False)
                group_e.write({'users': [(3, self.env.user.employee_id.id)]})
                group_e.write({'users': [(4, rec.delegations_employee_id.id)]})
            delegations_info = {'employee_id':self.env.user.employee_id.id,'delegated_employee_id':rec.delegations_employee_id.id,
                                'date_from':rec.date_from,'date_to':rec.date_to,'state':'draft','name':'test','date':datetime.now(),}
            filed = self.env['employee.delegations'].create(delegations_info)
            filed.onchange_method()
            filed.access_granted()
            notification_ids = [((0, 0, {
                'res_partner_id': rec.delegations_employee_id.id,
                'notification_type': 'inbox'}))]
            user_id = self.env.user.id
            message = ("You have a assigned a delegations from %s from %s to %s") % (self.env.user.employee_id.name,rec.date_from,rec.date_to)
            channel = self.env['mail.channel'].channel_get([rec.delegations_employee_id.id])
            channel_id = self.env['mail.channel'].browse(channel["id"])
            channel_id.message_post(author_id=user_id,
                                    body=(message),
                                    message_type='notification',
                                    subtype_xmlid="mail.mt_comment",
                                    notification_ids=notification_ids,
                                    partner_ids=[rec.delegations_employee_id.id],
                                    notify_by_email=False,
                                    )



    def _check_double_validation_rules(self, employees, state):
        super(HrLeave, self)._check_double_validation_rules(employees,state)
        print("here/************************************************************************************/")
        is_leave_user = self.user_has_groups('hr_holidays.group_hr_holidays_user')
        if state == 'validate1':
            # print(is_leave_user , "/*********************************************************************/")
            employees2 = [employee.leave_manager_id.id for employee in employees ]#employees.filtered(lambda employee: employee.leave_manager_id != self.env.user)
            print(employees2, '/________________________________________-------------__========000____-----')
            #
            # if  employees2 :
            #     if self.env.user in employees:
            #         raise AccessError(_('You cannot first approve a time off for %s, because you are not his time off manager', employees[0].name))
            # elif state == 'validate' and not is_leave_user:
            #     print("test +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")


