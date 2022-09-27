from odoo import api, fields, models, tools


class EmployeeRank(models.Model):
    _name = "hr.employee.rank"

    name = fields.Char()
    note = fields.Text()
    employee_ids = fields.One2many("hr.employee", "employee_rank_id", readonly=True)
    flight_ticket_type = fields.Selection(
        [("first", "First Class"), ("economy", "Economy Class"), ("business", "Business Class")]
    )
    internal_trip_stipend = fields.Float()
    external_trip_stipend = fields.Float()


class EmployeeBeneficiary(models.Model):
    _name = "hr.employee.beneficiary"

    name = fields.Char(string="Full Name", required=True)
    relation = fields.Char(required=True)
    gender = fields.Selection([("male", "Male"), ("female", "Female")], required=True)
    birth_date = fields.Date(required=True)
    note = fields.Text(required=True)
    employee_id = fields.Many2one("hr.employee", string="Related Employee")
    employee_phone = fields.Char(related="employee_id.work_phone")
    employee_department = fields.Many2one("hr.department", related="employee_id.department_id")
    approval_id = fields.Many2one("approval.request")
    phone_number = fields.Char(required=True)
    beneficiary_id = fields.Char(required=True)
    insurance_type_id = fields.Many2one('insurance.type')
    insurance_mount = fields.Float('Amount')

    @api.onchange('insurance_type_id')
    def onchange_insurance_type_id(self):
        self.insurance_mount = self.insurance_type_id.amount


class EmployeeHr(models.Model):
    _name = "hr.sector"
    name = fields.Char(translate=True)
    manager_id = fields.Many2one("hr.employee")
    employee_ids = fields.One2many("hr.employee", inverse_name="sector_id", readonly=True)


class HrEmployeePublic(models.AbstractModel):
    _inherit = "hr.employee.base"

    job_title = fields.Char(translate=True)
    arabic_name = fields.Char(compute="_compute_arabic_name", store=True)
    sector_id = fields.Many2one("hr.sector")
    employee_id_char = fields.Char()
    hijri_dob = fields.Char()
    hijri_id_expiration = fields.Char()
    joining_date = fields.Date(string="Joining Date")
    graduation_year = fields.Char()
    employee_beneficiary_ids = fields.One2many("hr.employee.beneficiary", inverse_name="employee_id")
    employee_rank_id = fields.Many2one("hr.employee.rank", string="Employee Grade")
    partner_id = fields.Many2one("res.partner")
    bank_id = fields.Many2one("res.partner.bank", string="Salary Bank")
    arabic_name_1 = fields.Char()
    arabic_name_2 = fields.Char()
    arabic_name_3 = fields.Char()
    arabic_name_4 = fields.Char()
    # ///////////////////////////////////////////////////
    employee_insurance_amount = fields.Float(string='Employee Insurance Amount')
    insurance_mount_total = fields.Float(string='Insurance Amount', store=True, readonly=True, compute='_amount_all')
    insurance_mount_total_day = fields.Float(string='Insurance Amount Per Day', store=True, readonly=True,
                                             compute='_amount_all')
    insurance_mount_total_month = fields.Float(string='Insurance Amount Per Month', store=True, readonly=True,
                                               compute='_amount_all')

    # ///////////////////////////////////////////////////////////
    @api.depends('employee_beneficiary_ids', 'employee_insurance_amount')
    def _amount_all(self):
        for rec in self:
            amount = 0.0
            for line in rec.employee_beneficiary_ids:
                amount += line.insurance_mount
            rec.update({
                'insurance_mount_total': amount + rec.employee_insurance_amount,
                'insurance_mount_total_day': (amount + rec.employee_insurance_amount) / 365,
                'insurance_mount_total_month': (amount + rec.employee_insurance_amount) / 12,
            })

    @api.depends(
        "arabic_name_1",
        "arabic_name_2",
        "arabic_name_3",
        "arabic_name_4",
    )
    def _compute_arabic_name(self):
        for record in self:
            record.arabic_name = f'{record.arabic_name_1 or ""} {record.arabic_name_2 or ""} {record.arabic_name_3 or ""} {record.arabic_name_4 or ""}'


class HrEmployeePrivate(models.Model):
    _inherit = "hr.employee"

    certificate = fields.Selection(
        selection_add=[
            ("diplma", "Diploma"),
            ("high_school", "High School"),
            ("phd", "PhD"),
        ]
    )
    signature_img = fields.Image("Signature")

    @api.depends('contract_ids.state', 'contract_ids.date_start')
    def _compute_first_contract_date(self):
        for employee in self:
            con = self.env['hr.contract'].search([('employee_id', '=', employee.id)], order='date_start asc', limit=1)
            employee.first_contract_date = con.date_start

    @api.model
    def create(self, vals):
        items = super().create(vals)
        items.action_send_new_joiner_email()
        return items

    def action_send_new_joiner_email(self):
        template_id = self.env.ref("nidlp_hr.mail_template_new_joiner")
        unsent_partners = self.mapped("name")
        send_to = ",".join(self.company_id.it_staff_ids.mapped("email"))
        ctx = {
            "email_to": send_to,
        }
        for record in self:
            template_id.sudo().send_mail(record.id, email_values=ctx)


class InsuranceType(models.Model):
    _name = 'insurance.type'

    name = fields.Char()
    amount = fields.Float()
