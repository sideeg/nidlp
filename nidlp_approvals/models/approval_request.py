from odoo import _, api, fields, models
from odoo.exceptions import UserError
import qrcode
import base64
from io import BytesIO
import datetime
import logging

_logger = logging.getLogger(__name__)


class ApprovalRequest(models.Model):
    _inherit = "approval.request"

    is_employee_certificate = fields.Boolean(related="category_id.is_employee_certificate")
    employee_certificate_type = fields.Selection(
        [("none", "To Whom It May concern"), ("specific", "Specific Entity"), ("salary_dom", "Salary Domiciliation")],
        string="Address To",
    )
    employee_certificate_address = fields.Char()
    employee_certificate_address_ar = fields.Char()
    approval_date = fields.Date(compute="_compute_approval_date", store=True)
    employee_id = fields.Many2one("hr.employee")
    is_change_department = fields.Boolean(related="category_id.is_change_department")
    is_change_sector = fields.Boolean(related="category_id.is_change_sector")
    is_change_job_title = fields.Boolean(related="category_id.is_change_job_title")
    is_change_housing_allowance = fields.Boolean(related="category_id.is_change_housing_allowance")
    is_change_transportation_allowance = fields.Boolean(related="category_id.is_change_transportation_allowance")
    is_change_other_allowance = fields.Boolean(related="category_id.is_change_other_allowance")
    is_change_wage = fields.Boolean(related="category_id.is_change_wage")
    is_self_serving = fields.Boolean(related="category_id.is_self_serving")
    is_change_status = fields.Boolean(related="category_id.is_change_status")
    new_department_id = fields.Many2one("hr.department")
    new_sector_id = fields.Many2one("hr.sector")
    current_sector_id = fields.Many2one("hr.sector", related="employee_id.sector_id")
    current_department_id = fields.Many2one("hr.department", related="employee_id.department_id")
    contract_id = fields.Many2one("hr.contract", compute="_compute_employee_data")
    currency_id = fields.Many2one("res.currency", related="contract_id.currency_id")
    current_wage = fields.Monetary(related="contract_id.wage")
    new_wage = fields.Float()
    current_housing_allowance = fields.Monetary(related="contract_id.l10n_sa_housing_allowance")
    new_housing_allowance = fields.Float()
    current_transportation_allowance = fields.Monetary(related="contract_id.l10n_sa_transportation_allowance")
    new_transportation_allowance = fields.Float()
    current_other_allowance = fields.Monetary(related="contract_id.l10n_sa_other_allowances")
    new_other_allowance = fields.Float()
    current_job_title = fields.Char(compute="_compute_employee_data")
    current_job_title_ar = fields.Char(compute="_compute_employee_data")
    new_job_title = fields.Char()
    new_job_title_ar = fields.Char()
    has_beneficiary = fields.Selection(related="category_id.has_beneficiary")
    employee_beneficiary_ids = fields.One2many("hr.employee.beneficiary", "approval_id")
    has_distance_riyadh = fields.Selection(related="category_id.has_distance_riyadh")
    has_country = fields.Selection(related="category_id.has_country")
    has_employee_class = fields.Selection(related="category_id.has_employee_class")
    has_external_stipend = fields.Selection(related="category_id.has_external_stipend")
    has_internal_stipend = fields.Selection(related="category_id.has_internal_stipend")
    country_id = fields.Many2one("res.country")
    distance_riyadh = fields.Selection(
        [
            ("40_79", "40-79 km"),
            ("79_more", "More than 79km"),
        ],
        string="Distance from Riyadh",
        default="79_more"
    )
    employee_rank_id = fields.Many2one(
        "hr.employee.rank", related="employee_id.employee_rank_id", string="Employee Grade"
    )
    flight_ticket_type = fields.Selection(related="employee_rank_id.flight_ticket_type")
    internal_trip_stipend = fields.Float(related="employee_rank_id.internal_trip_stipend")
    total_internal_trip_stipend = fields.Float(compute="compute_total_stipend")
    external_trip_stipend = fields.Float(related="employee_rank_id.external_trip_stipend")
    total_external_trip_stipend = fields.Float(compute="compute_total_stipend")
    trip_days = fields.Integer(compute="_compute_trip_days")
    is_trip = fields.Boolean(related="category_id.is_trip")
    trip_reason = fields.Char()
    is_vp_traveling = fields.Boolean()
    is_ceo_traveling = fields.Boolean()
    is_email_send = fields.Boolean(default=False)
    change_status_date = fields.Date()
    change_state_reason = fields.Char()
    salary_change_type = fields.Selection([("percentage", "Percentage"), ("flat", "Flat Amount")], default="flat")
    salary_change_percentage = fields.Float()
    expense_id = fields.Many2one(
        'hr.expense',
        string='Expense',
        readonly=True,
        tracking=True,
    )
    leave_id = fields.Many2one(
        'hr.leave',
        string='Leave',
        readonly=True,
        tracking=True,
    )
    qr_code = fields.Binary("QR Code", attachment=True, store=True)
    trip_type = fields.Selection(
        [("training", "Training"), ("workshop", "Workshop"), ("business_trip", "Business Trip")])

    def _create_expense(self):
        if self.is_trip:
            if not self.expense_id:
                if self.category_id.expenses_product_id:
                    expense = self.env['hr.expense'].create({
                        'name': self.category_id.expenses_product_id.name,
                        'product_id': self.category_id.expenses_product_id.id,
                        'quantity': 1,
                        'unit_amount': self.total_internal_trip_stipend if self.category_id.is_internal_trip else self.total_external_trip_stipend,
                        'account_id': self.category_id.expenses_product_id.property_account_expense_id.id or False,
                        'employee_id': self.employee_id.id,
                        'description': self.trip_reason,
                        'trip_id': self.id,
                    })
                    self.expense_id = expense.id
                else:
                    raise UserError(_("please select the expense product."))

    def _create_leave(self):
        if self.is_trip:
            if not self.leave_id:
                if self.category_id.leave_type_id:
                    leave = self.env['hr.leave'].create({
                        'holiday_status_id': self.category_id.leave_type_id.id,
                        'employee_id': self.employee_id.id,
                        'date_from': self.date_start - datetime.timedelta(days=1),
                        'date_to': self.date_end + datetime.timedelta(days=1),
                        'number_of_days': self.trip_days,
                    })
                    self.leave_id = leave.id
                else:
                    raise UserError(_("please select the leave type."))

    @api.onchange("salary_change_type")
    def on_change_salary_change_type(self):
        self.salary_change_percentage = 0
        self._on_change_salary_increase()

    @api.onchange("salary_change_percentage")
    def _on_change_salary_increase(self):
        percentage_added = self.salary_change_percentage / 100
        self.new_wage = self.current_wage * (1 + percentage_added)
        self.new_other_allowance = self.current_other_allowance * (1 + percentage_added)
        self.new_transportation_allowance = self.current_transportation_allowance * (1 + percentage_added)
        self.new_housing_allowance = self.current_housing_allowance * (1 + percentage_added)

    @api.depends("trip_days", "external_trip_stipend", "internal_trip_stipend")
    def compute_total_stipend(self):
        for record in self:
            record.total_external_trip_stipend = record.external_trip_stipend * (record.trip_days + 2)
            base_internal_stipend = record.internal_trip_stipend * record.trip_days
            if record.distance_riyadh == "40_79":
                base_internal_stipend += record.internal_trip_stipend
            elif record.distance_riyadh == "79_more":
                base_internal_stipend += record.internal_trip_stipend
            record.total_internal_trip_stipend = base_internal_stipend

    @api.depends("date_end", "date_start")
    def _compute_trip_days(self):
        for record in self:
            trip_days = False
            if all([record.is_trip, record.has_period != "no", record.date_start, record.date_end]):
                trip_days = (record.date_end - record.date_start).days + 1  # +1 because its inclusive
            record.trip_days = trip_days

    @api.constrains("date_end", "date_start")
    def _constraint_start_end_date(self):
        for record in self:
            if (
                    all([record.is_trip, record.has_period != "no", record.date_start, record.date_end])
                    and record.date_start > record.date_end
            ):
                raise UserError(_("Start date should not be greater than end date."))

    @api.constrains("date_end", "date_start")
    def _constraint_duplicate_trip(self):
        trips = self.env['approval.request'].search([('date_end', '>=', self.date_start),
                                                     ('date_start', '<=', self.date_start),
                                                     ('is_trip', '=', True),
                                                     ('employee_id', '=', self.employee_id.id),
                                                     ])
        for rec in trips:
            if rec and (rec != self):
                raise UserError(_("You have a norther trip in same date."))

    @api.onchange("employee_id")
    def _on_change_employee_id(self):
        self.employee_beneficiary_ids.filtered(lambda b: b.employee_id).update({"approval_id": False})
        self.update(
            {
                "employee_beneficiary_ids": [
                    (4, beneficiary.id, 0) for beneficiary in self.employee_id.employee_beneficiary_ids
                ]
            }
        )

    @api.depends("employee_id")
    def _compute_employee_data(self):
        for record in self:
            record.current_job_title = record.employee_id.job_title
            record.current_job_title_ar = record.employee_id.with_context(lang="ar_001").job_title
            # sudo since contract is a model readable only by HR group
            record.contract_id = record.employee_id.sudo().contract_id

    @api.depends("request_status")
    def _compute_approval_date(self):
        for record in self:
            record.approval_date = record.request_status == "approved" and fields.Date.today()

    def _issuer_sanity_check(self):
        if not self.env.company.employee_certificate_issuer or not self.env.company.company_ceo:
            raise UserError(_("Please select Employee Certificate Issuer and the CEO in the general settings!"))

    def print_salary_document(self):
        return self._print_document_helper("nidlp_hr.action_report_salary_report")

    def print_salary_transfer_document(self):
        return self._print_document_helper("nidlp_hr.action_report_salary_transfer_report")

    def _print_document_helper(self, ref):
        self.ensure_one()
        self._issuer_sanity_check()
        return (
            self.env.ref(ref)
            .with_context(lang="en_US")
            .report_action(
                self.employee_id,
                data={
                    "addressed_to": self.employee_certificate_address,
                    "addressed_to_ar": self.employee_certificate_address_ar,
                    "print_type": self._context.get("print_type"),
                    "employee_id": self.employee_id.id,
                    "issue_date": self.approval_date,
                },
            )
        )

    @api.model
    def create(self, vals):
        res = super().create(vals)
        if res.employee_certificate_type == "none":
            res.request_status = "approved"
        return res

    def _write(self, vals):
        if "employee_certificate_type" in vals and vals["employee_certificate_type"] == "none":
            vals["request_status"] = "approved"
        res = super()._write(vals)
        if "request_status" in vals and vals["request_status"] == "approved":
            # we use sudo because not everyone who creates/writes a request will have access to the employee/contract module
            self.sudo()._post_approval_hook()
        return res

    @api.depends("new_sector_id", "new_department_id", "request_owner_id", "employee_id")
    def _compute_approver_ids(self):
        if self.category_id.approval_level_type == "multi":
            self._create_multi_level_approval()
        else:
            super()._compute_approver_ids()

    def _sanity_check_department(self, is_transfer):
        if not self.employee_id:
            return False
        if not self.employee_id.department_id:
            raise UserError(_("Employee is not part of a department!"))
        elif not self.employee_id.department_id.manager_id:
            raise UserError(_("Employee's depeartment is missing the manager!"))
        elif not self.employee_id.department_id.manager_id.user_id:
            raise UserError(_("The Employee's Department Manager does not have a related user in the system!"))
        if is_transfer and self.new_department_id:
            if not self.new_department_id.manager_id:
                raise UserError(_("New Department has no manager selected! Please select a manager"))
            elif not self.new_department_id.manager_id.user_id:
                raise UserError(_("New Department Manager has no related user in the system!"))
            return self.new_department_id.manager_id.user_id
        return self.employee_id.department_id.manager_id.user_id.id

    def _sanity_check_sector_id(self, is_transfer):
        if not self.employee_id.sector_id:
            raise UserError(_("Employee is not part of a sector!"))
        elif not self.employee_id.sector_id.manager_id:
            raise UserError(_("Employee's information is missing the manager!"))
        elif not self.employee_id.sector_id.manager_id.user_id:
            raise UserError(_("The Employee's Manager does not have a related user in the system!"))
        if is_transfer and self.new_sector_id:
            if not self.new_sector_id.manager_id:
                raise UserError(_("New Sector has no manager selected! Please select a manager"))
            elif not self.new_sector_id.manager_id.user_id:
                raise UserError(_("New Sector Manager has no related user in the system!"))
            return self.new_sector_id.manager_id.user_id
        return self.employee_id.sector_id.manager_id.user_id.id

    def _sanity_check_line_manager(self):
        if not self.employee_id.parent_id:
            raise UserError(_("The Employee's Line Manager is not set!"))
        if not self.employee_id.parent_id.user_id:
            raise UserError(_("The Employee's line manager does not have a related user in the system!"))
        return self.employee_id.parent_id.user_id.id

    def _validate_sequence(self, approver):
        # need to make sure the sequence is respected.
        # the sequence is in the order of the creation which follows the same order the user puts in the settings.
        self.ensure_one()
        if not approver.is_ordered:
            return True
        for app in self.approver_ids:
            if app == approver:
                break
            if app.status != "approved" and (not app.group_id or app.group_id != approver.group_id):
                raise UserError(_("Previous approver has to approve first!"))
        return True

    def _create_approval_stack(self):
        # creates the approval stack,
        # for department managers/line managers/sector managers we first ensure a sanity check
        # for group approvals we add all of the group approvals to be needed
        self.ensure_one()
        vals = []
        seen_users = [1]  # lets not ask for Odoo but approval shall we

        def _create_approver_vals(user_id, group_id=False):
            seen_users.append(user_id)
            return {
                "user_id": user_id,
                "status": "new",
                "request_id": self.id,
                "group_id": group_id,
                "is_ordered": True,
            }

        for approval_level in self.category_id.approval_levels:
            if approval_level.type == "department_manager":
                if approval_level.is_transfer and not self.new_department_id:
                    continue
                user_id = self._sanity_check_department(approval_level.is_transfer)
                if user_id not in seen_users:
                    vals.append(_create_approver_vals(user_id))
            elif approval_level.type == "line_manager":
                user_id = self._sanity_check_line_manager()
                if user_id not in seen_users:
                    vals.append(_create_approver_vals(user_id))
            elif approval_level.type == "user":
                user_id = approval_level.user_id.id
                if user_id not in seen_users:
                    vals.append(_create_approver_vals(user_id))
            elif approval_level.type == "sector_manager":
                if approval_level.is_transfer and not self.new_sector_id:
                    continue
                user_id = self._sanity_check_sector_id(approval_level.is_transfer)
                if user_id not in seen_users:
                    vals.append(_create_approver_vals(user_id))
            elif approval_level.type == "group":
                for user in approval_level.group_id.users:
                    user_id = user.id
                    if user_id not in seen_users:
                        vals.append(_create_approver_vals(user_id, group_id=approval_level.group_id.id))
        return vals

    def _create_multi_level_approval(self):
        if not self.employee_id:
            return
        approval_stack = self._create_approval_stack()
        self.approver_ids = False
        for val in approval_stack:
            self.approver_ids += self.env["approval.approver"].new(
                val
            )  # new() cause this sometimes called in onchange.

    @api.constrains("employee_id", "request_status")
    def _employee_id_constraint(self):
        for request in self.filtered(lambda r: r.request_status == "new"):
            if not request.contract_id:
                raise UserError(_("This Employee does not have a running contract!"))
            if request.is_self_serving:
                continue
            if request.employee_id == self.env.user.employee_id:
                raise UserError(_("You cannot raise this type of approval for your self!"))
            if (
                    not self.env.user.has_group("nidlp_approvals.group_hr_approval")
                    and request.employee_id not in self.env.user.employee_id.child_ids
            ):
                raise UserError(
                    _("You cannot raise this type of approval unless you are part of HR or this employee's manager!")
                )

    def _post_approval_hook(self):
        # post approval hook to do some things after a certain request has been approved
        for record in self:
            if record.category_id.is_trip:
                record._notify_hr()

            if record.has_beneficiary == "required":
                record.employee_beneficiary_ids.write({"employee_id": record.employee_id.id})
            update_val = {}
            contract_vals = {}
            ar_values = {}
            if record.new_job_title:
                update_val["job_title"] = record.new_job_title
            if record.new_job_title_ar:
                ar_values["job_title"] = record.new_job_title_ar
            if record.new_department_id:
                update_val["department_id"] = record.new_department_id.id
            if record.new_sector_id:
                update_val["sector_id"] = record.new_sector_id
            if record.new_housing_allowance and record.is_change_housing_allowance:
                contract_vals["l10n_sa_housing_allowance"] = record.new_housing_allowance
            if record.new_transportation_allowance and record.is_change_transportation_allowance:
                contract_vals["l10n_sa_transportation_allowance"] = record.new_transportation_allowance
            if record.new_other_allowance and record.is_change_other_allowance:
                contract_vals["l10n_sa_other_allowances"] = record.new_other_allowance
            if record.new_wage and record.is_change_wage:
                contract_vals["wage"] = record.new_wage
            record.employee_id.write(update_val)
            record.employee_id.with_context(lang="ar_001").write(ar_values)
            record.contract_id.write(contract_vals)

    def _notify_hr(self):
        self.ensure_one()
        for user in self.env.ref("nidlp_approvals.group_hr_approval").users:
            activity_vals = {
                "user_id": user.id,
                "note": (f"{self.name} for {self.employee_id.name} Has been approved!"),
                "activity_type_id": self.env.ref("nidlp_approvals.mail_activity_data_trip_approval").id,
                "date_deadline": fields.Date.today(),
            }
            self.activity_schedule(**activity_vals)

    def _compute_multi_approval_request_status(self):
        for request in self:
            status_lst = request.mapped("approver_ids.status")
            if status_lst:
                minimal_approver = len(status_lst)
                if "cancel" in status_lst:
                    status = "cancel"
                elif "refused" in status_lst:
                    status = "refused"
                elif "new" in status_lst:
                    status = "new"
                elif status_lst.count("approved") == minimal_approver:
                    status = "approved"
                    request._create_expense()
                    request._create_leave()
                    request.generate_qr_code()
                else:
                    status = "pending"
            else:
                status = "new"
            request.request_status = status

    def _compute_request_status(self):
        if (
                self.category_id.approval_level_type != "multi"
        ):  # if multi_approval we will need different logic to compute the state
            super()._compute_request_status()
            if self.request_status == "approved":
                self._create_expense()
                self._create_leave()
                self.generate_qr_code()

        else:
            self._compute_multi_approval_request_status()

    def action_approve(self, approver=None):
        if not isinstance(approver, models.BaseModel):
            approver = self.mapped("approver_ids").filtered(lambda approver: approver.user_id == self.env.user)
        self._validate_sequence(approver)
        super().action_approve(approver)
        self._approve_group_approvals(approver)
        for rec in self:
            for r in rec.approver_ids:
                if rec.employee_id.parent_id.user_id and rec.employee_id.parent_id.user_id == r.user_id:
                    if rec.is_email_send == False:
                        rec.send_email()
                        rec.is_email_send = True

    def _approve_group_approvals(self, approver):
        # if an one member of a group approval approves a request, all other group approvals (Given same group) are also approved
        if approver.group_id:
            group_id = approver.group_id
            remaining_group_approvers = self.mapped("approver_ids").filtered(lambda a: a.group_id == group_id)
            for approver in remaining_group_approvers:
                super().with_user(approver.user_id).action_approve(approver)

    def generate_qr_code(self):
        name = str(self.employee_id.name)
        id = str(self.employee_id.identification_id)
        date = str(self.date_start)
        date_to = str(self.date_end)
        country = str(self.country_id.name)
        location = str(self.location)
        flight_ticket_type = str(self.flight_ticket_type)
        qr_str = name + "\n" + id + "\n" + date + "\n" + date_to + "\n" + country + "\n" + location + "\n" + flight_ticket_type
        if self.is_trip:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(qr_str)
            qr.make(fit=True)
            img = qr.make_image()
            temp = BytesIO()
            img.save(temp, format="PNG")
            qr_image = base64.b64encode(temp.getvalue())
            self.qr_code = qr_image

    def _find_mail_template(self):
        template_id = False
        template_id = self.category_id.template_id.id
        return template_id

    def action_trip_send(self):
        ''' Opens a wizard to compose an email, with relevant mail template loaded by default '''
        self.ensure_one()
        template_id = self._find_mail_template()
        lang = self.env.context.get('lang')
        template = self.env['mail.template'].browse(template_id)
        if template.lang:
            lang = template._render_lang(self.ids)[self.id]
        ctx = {
            'default_model': 'approval.request',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'custom_layout': "mail.mail_notification_paynow",
            'proforma': self.env.context.get('proforma', False),
            'force_email': True,
            'model_description': '/',
        }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }

    def send_email(self):
        for appraisal in self:
            template_id = self._find_mail_template()
            lang = self.env.context.get('lang')
            template = self.env['mail.template'].browse(template_id)

            # ////////////////////////////////////////////////////////////////
            report_template_id = self.env.ref(
                'nidlp_approvals.trip_report')._render_qweb_pdf(self.id)
            data_record = base64.b64encode(report_template_id[0])
            ir_values = {
                'name': "Trip.pdf",
                'type': 'binary',
                'datas': data_record,
                'store_fname': data_record,
                'mimetype': 'application/x-pdf',
            }
            data_id = self.env['ir.attachment'].create(ir_values)
            # ////////////////////////////////////////////////////////////////
            for rec in self:
                mail_values = {
                    'email_from': template.email_from,
                    'author_id': self.env.user.partner_id.id,
                    'model': None,
                    'res_id': None,
                    'subject': template.subject,
                    'body_html': template.body_html,
                    'auto_delete': True,
                    'email_to': template.email_to,
                    'email_cc': self.request_owner_id.email_formatted,
                    'attachment_ids': [(6, 0, [data_id.id])]
                    # self.category_id.partner_e_id.email
                    # (6, 0, [template.partner_to])
                }
                try:
                    template = self.env.ref('mail.mail_notification_light', raise_if_not_found=True)
                except ValueError:
                    _logger.warning(
                        'QWeb template mail.mail_notification_light not found when sending appraisal confirmed mails. Sending without layouting.')

                self.env['mail.mail'].sudo().create(mail_values).send()


class ApprovalApprover(models.Model):
    _inherit = "approval.approver"
    is_ordered = fields.Boolean()
    group_id = fields.Many2one("res.groups", string="Group")

    def _create_activity(self):
        # dont send an activity if the user is issuing a certain request
        for approver in self.filtered(lambda app: app.request_id.employee_certificate_type != "none"):
            approver.request_id.activity_schedule("approvals.mail_activity_data_approval", user_id=approver.user_id.id)


class HrExpense(models.Model):
    _inherit = "hr.expense"

    trip_id = fields.Many2one('approval.request', "request")
