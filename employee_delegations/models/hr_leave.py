
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


