from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SalaryReport(models.AbstractModel):
    _name = "report.nidlp_hr.salary_report"

    def _get_report_values(self, docids, data=None):
        employee_id = data.get("employee_id") or (docids and docids[0])
        print_type = data.get("print_type", "no_salary")
        addressed_to = data.get("addressed_to") or "Whom it May Concern"
        addressed_to_ar = data.get("addressed_to_ar") or "من يهمه الأمر"
        date = data.get("issue_date")
        date = fields.Date.to_date(date) if date else fields.Date.today()
        employee = self.env["hr.employee"].browse(employee_id)
        issued_by = (
            employee != self.env.company.employee_certificate_issuer and self.env.company.employee_certificate_issuer
        ) or self.env.company.company_ceo

        contract_id = employee.sudo().contract_id

        if not contract_id:
            raise UserError(_(f"Selected Employee ({employee.sudo().name}) does not have a running contract!"))
        return {
            "doc_ids": employee.ids,
            "doc_model": "hr.employee",
            "docs": employee,
            "print_type": print_type,
            "company": self.env.company,
            "date": date,
            "contract": contract_id,
            "issued_by": issued_by,
            "addressed_to": {"en": addressed_to, "ar": addressed_to_ar},
        }


class SalaryTransferReport(models.AbstractModel):
    _name = "report.nidlp_hr.salary_transfer_report"
    _inherit = "report.nidlp_hr.salary_report"
