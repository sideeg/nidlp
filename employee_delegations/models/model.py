from odoo import fields, models, api
from datetime import datetime


class EmployeeDelegations(models.Model):
    _name = 'employee.delegations'
    _description = 'Employee Delegations'
    _rec_name = 'state'
    name = fields.Html()
    employee_id = fields.Many2one('hr.employee', 'Employee')
    delegated_employee_id = fields.Many2one('hr.employee', 'Delegated Employee')
    date = fields.Date('Delegations Date')
    date_from = fields.Date('Date From')
    date_to = fields.Date('Date To')
    state = fields.Selection(
        string='Status',
        selection=[('draft', 'Draft'),
                   ('access_granted', 'Access Granted'),
                   ('access_returned', 'Access Return'),
                   ], required=True, readonly=True, copy=False,tracking=True, default='draft')

    group_ids = fields.Many2many('res.groups', 'delegations_id')
    copy_group_ids = fields.Many2many('res.groups', 'delegations_id')
    readonly = fields.Boolean(default=False)
    is_granted = fields.Boolean('is granted', readonly=True,default=False)
    # is_leave_user = fields.Boolean('is_leave_user',readonly=True,default=False)
    @api.onchange('delegated_employee_id')
    def onchange_method(self):
        self.group_ids = False
        employee_groups = []
        delegated_employee_groups = []
        diff = []
        if self.delegated_employee_id:
            for r in self.employee_id.user_id.groups_id:
                employee_groups.append(r.id)
                if r.name == 'hr_holidays.group_hr_holidays_user':
                    # self.is_leave_user = True
                    group_e = self.env.ref('hr_holidays.group_hr_holidays_user', False)
                    group_e.write({'users': [(3, self.env.user.employee_id.id)]})

            for re in self.delegated_employee_id.user_id.groups_id:
                delegated_employee_groups.append(re.id)
            diff = self.diff(employee_groups, delegated_employee_groups)
            if len(diff) > 0:
                for group_id in diff:
                    self.group_ids = [(4, group_id)]

    def diff(self, li1, li2):
        return list(set(li1) - set(li2)) + list(set(li2) - set(li1))

    def access_granted(self):
        for rec in self:
            if rec.group_ids :

                for group_id in rec.group_ids:
                    rec.delegated_employee_id.user_id.groups_id = [(4, group_id.id)]
                    rec.employee_id.user_id.groups_id = [(3, group_id.id)]
                    if rec.name == 'hr_holidays.group_hr_holidays_user':
                        # self.is_leave_user = True
                        group_e = self.env.ref('hr_holidays.group_hr_holidays_user', False)
                        group_e.write({'users': [(3, rec.delegated_employee_id.user_id)]})

                rec.readonly = True
                rec.is_granted = True
                rec.state = 'access_granted'
                print(rec.employee_id.user_id.groups_id,'**************************************************')

        # return {
        #     'type': 'ir.actions.client',
        #     'tag': 'reload',
        # }

    def access_returned(self):
        for rec in self:
            if rec.group_ids :
                for group_id in rec.group_ids:
                    rec.delegated_employee_id.user_id.groups_id = [(3, group_id.id)]
                    rec.employee_id.user_id.groups_id = [(4, group_id.id)]

                rec.readonly = True
                rec.is_granted = False
                rec.state = 'access_returned'
                print(rec.employee_id.user_id.groups_id,'**************************************************')
        # return {
        #     'type': 'ir.actions.client',
        #     'tag': 'reload',
        # }

    def set_to_draft(self):
        for rec in self:
            rec.readonly = False
            rec.state = 'draft'

    def cron_access_returned(self):
        for rec in self:
            if rec.date_to < datetime.now() :
                rec.access_returned()
class ResGroups(models.Model):
    _inherit = 'res.groups'
    delegations_id = fields.Many2one('employee.delegations')
