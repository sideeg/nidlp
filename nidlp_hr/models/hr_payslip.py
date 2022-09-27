from odoo import api, fields, models, tools


class HRPayslip(models.Model):
    _inherit = "hr.payslip"

    def action_print_wps(self):
        return self.env.ref("nidlp_hr.action_wps_report").report_action(self)

    def print_wps_report(self):
        options = {"col_number": 13, "col_size": 20, "col_sizing": [20, 50, 20, 20, 20, 20, 20, 40, 20, 20, 20, 20, 30]}
        rows = [
            {
                "style": {"bold": True, "pattern": 1, "bg_color": "#E0E0E0", "align": "center", "reading_order": 2},
                "items": [
                    "Net Salary",
                    "Beneficiary Account",
                    "Beneficiary Name 1",
                    "Beneficiary Name 2",
                    "Beneficiary Name 3",
                    "Beneficiary Name 4",
                    "Beneficiary Bank",
                    "Payment Description Optional",
                    "Basic Salary",
                    "Housing Allowance",
                    "Other Earnings",
                    "Deductions",
                    "Beneficiary ID",
                ],
            }
        ]
        for payslip in self:
            employee_id = payslip.employee_id
            net = payslip.line_ids.filtered(lambda r: r.code == "NET").total
            rows.append(
                {
                    "style": {"reading_order": 2},
                    "items": [
                        net,
                        employee_id.bank_id.acc_number or "",
                        employee_id.arabic_name_1 or "",
                        employee_id.arabic_name_2 or "",
                        employee_id.arabic_name_3 or "",
                        employee_id.arabic_name_4 or "",
                        employee_id.bank_id.bank_name or "",
                        "",
                        net,
                        0.0,
                        0.0,
                        0.0,
                        employee_id.identification_id or "",
                    ],
                }
            )
        return options, rows
